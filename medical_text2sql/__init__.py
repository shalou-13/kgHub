"""
Medical Text-to-SQL System

A system for converting natural language questions to SQL queries
specifically designed for medical databases.
"""

__version__ = "1.0.0"
__author__ = "kgHub Team"

from .config import config
from .schema_manager import SchemaManager
from .prompt_builder import PromptBuilder
from .llm_client import Text2SQLConverter
from .sql_executor import SQLSecurityFilter, SQLExecutor
from .feedback import FeedbackCollector

__all__ = [
    'config',
    'SchemaManager',
    'PromptBuilder',
    'Text2SQLConverter',
    'SQLSecurityFilter',
    'SQLExecutor',
    'FeedbackCollector',
]
