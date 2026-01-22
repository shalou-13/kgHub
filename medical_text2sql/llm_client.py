"""LLM calling and SQL extraction module."""
import re
import logging
from typing import Optional, Dict, Any
import requests
from config import config

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for calling various LLM APIs."""
    
    def __init__(self):
        """Initialize LLM client."""
        self.provider = config.LLM_PROVIDER
        self.api_key = config.LLM_API_KEY
        self.api_base = config.LLM_API_BASE
        self.model = config.LLM_MODEL
        
    def call_openai(self, prompt: str) -> Optional[str]:
        """Call OpenAI API.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            LLM response text or None if failed
        """
        try:
            import openai
            
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful medical database assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more consistent SQL generation
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def call_generic_api(self, prompt: str) -> Optional[str]:
        """Call generic LLM API with OpenAI-compatible format.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            LLM response text or None if failed
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful medical database assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Generic API call failed: {e}")
            return None
    
    def call_llm(self, prompt: str) -> Optional[str]:
        """Call LLM based on configured provider.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            LLM response text or None if failed
        """
        if self.provider == "openai":
            return self.call_openai(prompt)
        else:
            # For other providers (tongyi, xunfei, local), use generic API
            return self.call_generic_api(prompt)


class SQLExtractor:
    """Extracts SQL from LLM responses."""
    
    @staticmethod
    def extract_sql(response: str) -> Optional[str]:
        """Extract SQL from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Extracted SQL or None if not found
        """
        if not response:
            return None
        
        # Try to find SQL between # markers
        pattern = r'#(.*?)#'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            sql = matches[0].strip()
            logger.info(f"Extracted SQL using # markers: {sql[:100]}...")
            return sql
        
        # Try to find SQL code blocks
        pattern = r'```sql\s*(.*?)\s*```'
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        
        if matches:
            sql = matches[0].strip()
            logger.info(f"Extracted SQL from code block: {sql[:100]}...")
            return sql
        
        # Try to find SELECT statements
        pattern = r'(SELECT\s+.*?;?)\s*$'
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        
        if matches:
            sql = matches[0].strip()
            if not sql.endswith(';'):
                sql += ';'
            logger.info(f"Extracted SQL from SELECT pattern: {sql[:100]}...")
            return sql
        
        # If no pattern matches, return the whole response as potential SQL
        logger.warning("Could not extract SQL using patterns, returning full response")
        return response.strip()
    
    @staticmethod
    def clean_sql(sql: str) -> str:
        """Clean and normalize SQL query.
        
        Args:
            sql: Raw SQL query
            
        Returns:
            Cleaned SQL query
        """
        # Remove extra whitespace
        sql = ' '.join(sql.split())
        
        # Ensure it ends with semicolon
        if not sql.endswith(';'):
            sql += ';'
        
        return sql


class Text2SQLConverter:
    """Main class for converting natural language to SQL."""
    
    def __init__(self):
        """Initialize converter."""
        self.llm_client = LLMClient()
        self.sql_extractor = SQLExtractor()
        
    def convert(self, prompt: str) -> Optional[str]:
        """Convert natural language to SQL using LLM.
        
        Args:
            prompt: Complete prompt including question and context
            
        Returns:
            Extracted SQL query or None if failed
        """
        # Call LLM
        response = self.llm_client.call_llm(prompt)
        
        if not response:
            logger.error("LLM call failed")
            return None
        
        logger.info(f"LLM response: {response[:200]}...")
        
        # Extract SQL
        sql = self.sql_extractor.extract_sql(response)
        
        if sql:
            sql = self.sql_extractor.clean_sql(sql)
            logger.info(f"Final SQL: {sql}")
            return sql
        
        logger.error("Failed to extract SQL from response")
        return None
