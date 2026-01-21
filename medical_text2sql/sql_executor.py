"""SQL security filtering and execution module."""
import re
import logging
from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from config import config

logger = logging.getLogger(__name__)


class SQLSecurityFilter:
    """Filters and validates SQL queries for security."""
    
    # Blacklisted SQL keywords (DDL/DML operations)
    BLACKLIST_KEYWORDS = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE',
        'TRUNCATE', 'REPLACE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE'
    ]
    
    def __init__(self, allowed_tables: List[str]):
        """Initialize security filter.
        
        Args:
            allowed_tables: List of table names that are allowed to be queried
        """
        self.allowed_tables = allowed_tables
        
    def check_blacklist(self, sql: str) -> Tuple[bool, Optional[str]]:
        """Check if SQL contains blacklisted keywords.
        
        Args:
            sql: SQL query to check
            
        Returns:
            Tuple of (is_safe, error_message)
        """
        sql_upper = sql.upper()
        
        for keyword in self.BLACKLIST_KEYWORDS:
            # Use word boundary to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"SQL contains forbidden keyword: {keyword}"
        
        return True, None
    
    def check_allowed_tables(self, sql: str) -> Tuple[bool, Optional[str]]:
        """Check if SQL only accesses allowed tables.
        
        Args:
            sql: SQL query to check
            
        Returns:
            Tuple of (is_safe, error_message)
        """
        # Extract table names from SQL (simple pattern matching)
        # This is a simplified version - production code should use SQL parsing
        sql_upper = sql.upper()
        
        # Find FROM and JOIN clauses
        from_pattern = r'FROM\s+(\w+)'
        join_pattern = r'JOIN\s+(\w+)'
        
        from_matches = re.findall(from_pattern, sql_upper)
        join_matches = re.findall(join_pattern, sql_upper)
        
        all_tables = from_matches + join_matches
        
        # Check if all tables are in allowed list
        allowed_upper = [t.upper() for t in self.allowed_tables]
        
        for table in all_tables:
            if table not in allowed_upper:
                return False, f"Access to table '{table}' is not allowed"
        
        return True, None
    
    def add_result_limit(self, sql: str, max_rows: int = None) -> str:
        """Add LIMIT clause to SQL if not present.
        
        Args:
            sql: SQL query
            max_rows: Maximum number of rows (default from config)
            
        Returns:
            SQL with LIMIT clause
        """
        if max_rows is None:
            max_rows = config.MAX_RESULT_ROWS
        
        sql_upper = sql.upper()
        
        # Check if LIMIT already exists
        if 'LIMIT' in sql_upper:
            return sql
        
        # Remove trailing semicolon if present
        sql = sql.rstrip(';').strip()
        
        # Add LIMIT clause
        sql = f"{sql} LIMIT {max_rows};"
        
        return sql
    
    def rewrite_select_all(self, sql: str) -> str:
        """Rewrite SELECT * to select specific columns.
        
        Args:
            sql: SQL query
            
        Returns:
            Rewritten SQL query
        """
        # This is a simplified version
        # In production, you would parse the SQL and replace * with actual columns
        # For now, we'll leave this as a placeholder
        return sql
    
    def validate_and_sanitize(self, sql: str) -> Tuple[bool, Optional[str], str]:
        """Validate and sanitize SQL query.
        
        Args:
            sql: SQL query to validate
            
        Returns:
            Tuple of (is_safe, error_message, sanitized_sql)
        """
        # Check blacklist
        is_safe, error = self.check_blacklist(sql)
        if not is_safe:
            logger.warning(f"SQL failed blacklist check: {error}")
            return False, error, sql
        
        # Check allowed tables
        is_safe, error = self.check_allowed_tables(sql)
        if not is_safe:
            logger.warning(f"SQL failed table check: {error}")
            return False, error, sql
        
        # Add result limit
        sql = self.add_result_limit(sql)
        
        logger.info("SQL passed security checks")
        return True, None, sql


class SQLExecutor:
    """Executes SQL queries against the database."""
    
    def __init__(self, engine: Engine, security_filter: SQLSecurityFilter):
        """Initialize SQL executor.
        
        Args:
            engine: SQLAlchemy engine
            security_filter: Security filter instance
        """
        self.engine = engine
        self.security_filter = security_filter
        
    def execute_query(self, sql: str) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
        """Execute SQL query.
        
        Args:
            sql: SQL query to execute
            
        Returns:
            Tuple of (success, results, error_message)
            results is a list of dictionaries representing rows
        """
        # Validate and sanitize SQL
        is_safe, error, sanitized_sql = self.security_filter.validate_and_sanitize(sql)
        
        if not is_safe:
            return False, None, error
        
        # Execute query
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sanitized_sql))
                
                # Fetch results
                rows = []
                for row in result:
                    # Convert row to dictionary
                    row_dict = dict(row._mapping)
                    rows.append(row_dict)
                
                logger.info(f"Query executed successfully, returned {len(rows)} rows")
                return True, rows, None
                
        except SQLAlchemyError as e:
            error_msg = str(e)
            logger.error(f"Query execution failed: {error_msg}")
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def execute_with_retry(self, sql: str, llm_converter, 
                          prompt_builder, schema_manager, 
                          question: str, max_retries: int = None) -> Tuple[bool, Optional[List[Dict]], Optional[str], str]:
        """Execute SQL with retry on failure.
        
        Args:
            sql: Initial SQL query
            llm_converter: LLM converter instance for retry
            prompt_builder: Prompt builder instance
            schema_manager: Schema manager instance
            question: Original question
            max_retries: Maximum retry count (default from config)
            
        Returns:
            Tuple of (success, results, error_message, final_sql)
        """
        if max_retries is None:
            max_retries = config.MAX_RETRY_COUNT if config.ENABLE_SQL_RETRY else 0
        
        current_sql = sql
        
        for attempt in range(max_retries + 1):
            success, results, error = self.execute_query(current_sql)
            
            if success:
                return True, results, None, current_sql
            
            # If failed and retries available, try to fix
            if attempt < max_retries:
                logger.info(f"Query failed, attempting retry {attempt + 1}/{max_retries}")
                
                # Build retry prompt with error information
                retry_prompt = self._build_retry_prompt(
                    question, current_sql, error,
                    prompt_builder, schema_manager
                )
                
                # Get corrected SQL from LLM
                corrected_sql = llm_converter.convert(retry_prompt)
                
                if corrected_sql:
                    current_sql = corrected_sql
                    logger.info(f"Retry SQL: {current_sql}")
                else:
                    logger.error("Failed to generate corrected SQL")
                    break
        
        return False, None, error, current_sql
    
    def _build_retry_prompt(self, question: str, failed_sql: str, 
                           error: str, prompt_builder, schema_manager) -> str:
        """Build prompt for retry attempt.
        
        Args:
            question: Original question
            failed_sql: SQL that failed
            error: Error message (sanitized)
            prompt_builder: Prompt builder instance
            schema_manager: Schema manager instance
            
        Returns:
            Retry prompt
        """
        # Sanitize error message (hide sensitive information)
        sanitized_error = self._sanitize_error(error)
        
        # Get relevant tables
        tables = schema_manager.select_relevant_tables(question)
        schema_text = schema_manager.render_schema_text(tables)
        
        retry_instruction = f"""之前生成的 SQL 查询执行失败。

原始问题：{question}

失败的 SQL：
{failed_sql}

错误信息：
{sanitized_error}

请修正这个 SQL 查询，确保：
1. 语法正确
2. 表名和字段名正确
3. 避免导致错误的问题

请生成修正后的 SQL 查询。"""
        
        # Build full prompt with schema context
        full_prompt = f"{prompt_builder.build_instruction()}\n\n数据库结构信息：\n{schema_text}\n\n{retry_instruction}\n\n请只输出一条 SQL 查询，用 # 包裹。"
        
        return full_prompt
    
    @staticmethod
    def _sanitize_error(error: str) -> str:
        """Sanitize error message to hide sensitive information.
        
        Args:
            error: Raw error message
            
        Returns:
            Sanitized error message
        """
        # Remove potential sensitive information like table structures, paths, etc.
        # This is a simplified version
        sanitized = error[:500]  # Limit length
        
        # Remove common sensitive patterns
        sanitized = re.sub(r'at \S+:\d+', '', sanitized)  # File paths
        sanitized = re.sub(r'File "[^"]+",', '', sanitized)  # File names
        
        return sanitized
