"""FastAPI web service for medical Text-to-SQL."""
import logging
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

from config import config
from schema_manager import SchemaManager
from prompt_builder import PromptBuilder
from llm_client import Text2SQLConverter
from sql_executor import SQLSecurityFilter, SQLExecutor
from feedback import FeedbackCollector

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Text-to-SQL API",
    description="Convert natural language questions to SQL queries for medical databases",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
engine = None
schema_manager = None
prompt_builder = None
llm_converter = None
sql_executor = None
feedback_collector = None


# Request/Response models
class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    question: str = Field(..., description="Natural language question in Chinese")
    max_examples: int = Field(5, description="Maximum number of few-shot examples")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "统计2024年住院超过7天的成年患者人数",
                "max_examples": 5
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    success: bool = Field(..., description="Whether the query was successful")
    query_id: str = Field(..., description="Unique query identifier")
    sql: Optional[str] = Field(None, description="Generated SQL query")
    results: Optional[List[Dict]] = Field(None, description="Query results")
    result_count: Optional[int] = Field(None, description="Number of results returned")
    error: Optional[str] = Field(None, description="Error message if failed")


class FeedbackRequest(BaseModel):
    """Request model for feedback endpoint."""
    query_id: str = Field(..., description="Query ID to provide feedback for")
    feedback: str = Field(..., description="Feedback label: correct/partial/wrong")
    corrected_sql: Optional[str] = Field(None, description="Corrected SQL if applicable")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "20240101_120000_123456",
                "feedback": "correct",
                "corrected_sql": None
            }
        }


class StatsResponse(BaseModel):
    """Response model for stats endpoint."""
    stats: Dict = Field(..., description="Feedback statistics")


@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup."""
    global engine, schema_manager, prompt_builder, llm_converter, sql_executor, feedback_collector
    
    try:
        # Initialize database connection
        logger.info("Initializing database connection...")
        engine = create_engine(config.database_url, pool_pre_ping=True)
        
        # Initialize schema manager
        logger.info("Initializing schema manager...")
        schema_manager = SchemaManager(engine)
        
        # Try to load schema from file, otherwise extract from database
        try:
            schema_manager.load_schema_from_file("medical_schema.json")
        except FileNotFoundError:
            logger.info("Schema file not found, extracting from database...")
            schema_manager.extract_schema()
            schema_manager.save_schema_to_file("medical_schema.json")
        
        # Initialize prompt builder
        logger.info("Initializing prompt builder...")
        prompt_builder = PromptBuilder(db_type=config.DB_TYPE)
        
        # Initialize LLM converter
        logger.info("Initializing LLM converter...")
        llm_converter = Text2SQLConverter()
        
        # Initialize SQL executor with security filter
        logger.info("Initializing SQL executor...")
        allowed_tables = schema_manager.get_all_table_names()
        security_filter = SQLSecurityFilter(allowed_tables)
        sql_executor = SQLExecutor(engine, security_filter)
        
        # Initialize feedback collector
        logger.info("Initializing feedback collector...")
        feedback_collector = FeedbackCollector("data/feedback_log.jsonl")
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Medical Text-to-SQL API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/query",
            "feedback": "/feedback",
            "stats": "/stats",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Convert natural language question to SQL and execute.
    
    Args:
        request: Query request with question
        
    Returns:
        Query response with SQL and results
    """
    try:
        logger.info(f"Received query: {request.question}")
        
        # Select relevant tables
        relevant_tables = schema_manager.select_relevant_tables(request.question)
        
        # Render schema
        schema_text = schema_manager.render_schema_text(relevant_tables)
        
        # Build prompt
        prompt = prompt_builder.build_full_prompt(
            request.question,
            schema_text,
            request.max_examples
        )
        
        # Convert to SQL
        sql = llm_converter.convert(prompt)
        
        if not sql:
            query_id = feedback_collector.log_query(
                request.question, "", False, error="Failed to generate SQL"
            )
            return QueryResponse(
                success=False,
                query_id=query_id,
                error="Failed to generate SQL from question"
            )
        
        # Execute SQL with retry
        success, results, error, final_sql = sql_executor.execute_with_retry(
            sql, llm_converter, prompt_builder, 
            schema_manager, request.question
        )
        
        # Log query
        query_id = feedback_collector.log_query(
            request.question, final_sql, success, 
            results=results, error=error
        )
        
        if success:
            return QueryResponse(
                success=True,
                query_id=query_id,
                sql=final_sql,
                results=results,
                result_count=len(results)
            )
        else:
            return QueryResponse(
                success=False,
                query_id=query_id,
                sql=final_sql,
                error=error
            )
            
    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for a query.
    
    Args:
        request: Feedback request
        
    Returns:
        Success message
    """
    try:
        feedback_collector.add_feedback(
            request.query_id,
            request.feedback,
            request.corrected_sql
        )
        
        return {
            "success": True,
            "message": f"Feedback recorded for query {request.query_id}"
        }
        
    except Exception as e:
        logger.error(f"Failed to submit feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get feedback statistics.
    
    Returns:
        Feedback statistics
    """
    try:
        stats = feedback_collector.get_feedback_stats()
        return StatsResponse(stats=stats)
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
