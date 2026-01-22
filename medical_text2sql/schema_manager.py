"""Schema management and retrieval module for medical database."""
import json
import logging
from typing import Dict, List, Optional, Tuple
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
import jieba

from config import config

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema extraction, storage, and retrieval."""
    
    def __init__(self, engine: Engine):
        """Initialize schema manager.
        
        Args:
            engine: SQLAlchemy engine for database connection
        """
        self.engine = engine
        self.schema_cache: Dict[str, Dict] = {}
        self.table_keywords: Dict[str, List[str]] = {}
        
    def extract_schema(self) -> Dict[str, Dict]:
        """Extract schema information from database.
        
        Returns:
            Dictionary mapping table names to their schema information
        """
        inspector = inspect(self.engine)
        schema = {}
        
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                col_info = {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column.get("nullable", True),
                    "comment": column.get("comment", "")
                }
                columns.append(col_info)
            
            # Try to get table comment
            table_comment = ""
            try:
                with self.engine.connect() as conn:
                    if config.DB_TYPE == "postgresql":
                        result = conn.execute(text(
                            """SELECT obj_description(oid) as comment 
                               FROM pg_class 
                               WHERE relname = :table_name"""
                        ), {"table_name": table_name})
                    elif config.DB_TYPE == "mysql":
                        result = conn.execute(text(
                            """SELECT table_comment as comment 
                               FROM information_schema.tables 
                               WHERE table_schema = DATABASE() 
                               AND table_name = :table_name"""
                        ), {"table_name": table_name})
                    row = result.fetchone()
                    if row and row[0]:
                        table_comment = row[0]
            except Exception as e:
                logger.warning(f"Failed to get comment for table {table_name}: {e}")
            
            schema[table_name] = {
                "table": table_name,
                "comment": table_comment,
                "columns": columns
            }
        
        self.schema_cache = schema
        return schema
    
    def save_schema_to_file(self, filepath: str):
        """Save extracted schema to JSON file.
        
        Args:
            filepath: Path to save schema JSON
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.schema_cache, f, ensure_ascii=False, indent=2)
        logger.info(f"Schema saved to {filepath}")
    
    def load_schema_from_file(self, filepath: str):
        """Load schema from JSON file.
        
        Args:
            filepath: Path to schema JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            self.schema_cache = json.load(f)
        logger.info(f"Schema loaded from {filepath}")
    
    def add_medical_semantics(self, table_name: str, comment: str = None, 
                            column_comments: Dict[str, str] = None):
        """Add medical semantic information to schema.
        
        Args:
            table_name: Name of the table
            comment: Chinese description of the table
            column_comments: Dictionary mapping column names to Chinese descriptions
        """
        if table_name not in self.schema_cache:
            logger.warning(f"Table {table_name} not found in schema")
            return
        
        if comment:
            self.schema_cache[table_name]["comment"] = comment
        
        if column_comments:
            for column in self.schema_cache[table_name]["columns"]:
                if column["name"] in column_comments:
                    column["comment"] = column_comments[column["name"]]
    
    def set_table_keywords(self, table_name: str, keywords: List[str]):
        """Set keywords for table for rule-based retrieval.
        
        Args:
            table_name: Name of the table
            keywords: List of Chinese keywords associated with this table
        """
        self.table_keywords[table_name] = keywords
    
    def select_relevant_tables(self, question: str, max_tables: int = 5) -> List[str]:
        """Select relevant tables based on question using rule-based matching.
        
        Args:
            question: User's natural language question
            max_tables: Maximum number of tables to return
            
        Returns:
            List of relevant table names
        """
        # Tokenize question
        words = list(jieba.cut(question))
        
        # Score each table based on keyword overlap
        scores = {}
        for table_name, keywords in self.table_keywords.items():
            score = sum(1 for word in words if word in keywords)
            if score > 0:
                scores[table_name] = score
        
        # Sort by score and return top tables
        sorted_tables = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected_tables = [table for table, _ in sorted_tables[:max_tables]]
        
        # If no matches, return all tables (or a default set)
        if not selected_tables:
            selected_tables = list(self.schema_cache.keys())[:max_tables]
        
        logger.info(f"Selected tables for question: {selected_tables}")
        return selected_tables
    
    def render_schema_text(self, table_names: List[str]) -> str:
        """Render schema information as text for prompt.
        
        Args:
            table_names: List of table names to include
            
        Returns:
            Formatted schema text
        """
        schema_lines = []
        
        for table_name in table_names:
            if table_name not in self.schema_cache:
                continue
            
            table_info = self.schema_cache[table_name]
            comment = table_info.get("comment", "")
            
            # Table header
            if comment:
                schema_lines.append(f"表 {table_name}（{comment}）：")
            else:
                schema_lines.append(f"表 {table_name}：")
            
            # Columns
            for col in table_info["columns"]:
                col_comment = col.get("comment", "")
                if col_comment:
                    schema_lines.append(f"  - {col['name']}: {col_comment}")
                else:
                    schema_lines.append(f"  - {col['name']}: {col['type']}")
            
            schema_lines.append("")  # Empty line between tables
        
        return "\n".join(schema_lines)
    
    def get_all_table_names(self) -> List[str]:
        """Get all table names in schema.
        
        Returns:
            List of all table names
        """
        return list(self.schema_cache.keys())
