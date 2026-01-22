"""Database initialization script."""
import logging
from sqlalchemy import create_engine, text
from config import config
from database_schema import CREATE_TABLES_SQL_MYSQL, INSERT_SAMPLE_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with sample schema and data."""
    try:
        # Create engine
        engine = create_engine(config.database_url)
        
        logger.info(f"Connecting to database: {config.DB_TYPE}")
        
        # Get appropriate SQL based on database type
        if config.DB_TYPE == "mysql":
            create_sql = CREATE_TABLES_SQL_MYSQL
        else:
            # For PostgreSQL
            from database_schema import CREATE_TABLES_SQL
            create_sql = CREATE_TABLES_SQL
        
        # Execute table creation
        with engine.connect() as conn:
            # Split and execute each statement
            statements = create_sql.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        logger.warning(f"Statement execution warning: {e}")
            
            logger.info("Database tables created successfully")
            
            # Insert sample data
            data_statements = INSERT_SAMPLE_DATA.split(';')
            
            for statement in data_statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        logger.warning(f"Sample data insertion warning: {e}")
            
            logger.info("Sample data inserted successfully")
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    init_database()
