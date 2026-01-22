"""Prompt construction module for Text-to-SQL."""
import logging
from typing import List, Dict, Optional
from fewshot_data import FEWSHOT_EXAMPLES, MEDICAL_TERMINOLOGY

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds prompts for LLM-based Text-to-SQL conversion."""
    
    # Instruction template
    INSTRUCTION_TEMPLATE = """你是医疗数据库助理，负责把用户的自然语言问题转换成 SQL 查询。
请遵守以下规则：
1. 只使用我提供的数据库表和字段，不要猜测不存在的字段。
2. 只输出一条完整的 SQL 查询，不要包含任何解释文字。
3. SQL 语句必须以 # 开始和结束，例如：#SELECT ...#
4. 确保 SQL 语法正确，适用于 {db_type} 数据库。
5. 对于时间查询，使用标准的 SQL 日期函数。
6. 查询结果应该限制在合理范围内，必要时添加 LIMIT 子句。
"""

    # Time expression guidelines
    TIME_GUIDELINES = """
时间表达式规范：
- "过去 N 天" 应使用: WHERE event_time >= CURRENT_DATE - INTERVAL 'N day'
- "最近 N 天" 应使用: WHERE event_time >= CURRENT_DATE - INTERVAL 'N day'
- "2024年" 应使用: WHERE event_time >= '2024-01-01' AND event_time < '2025-01-01'
- "本月" 应使用: WHERE EXTRACT(MONTH FROM event_time) = EXTRACT(MONTH FROM CURRENT_DATE)
"""
    
    def __init__(self, db_type: str = "postgresql"):
        """Initialize prompt builder.
        
        Args:
            db_type: Database type (postgresql or mysql)
        """
        self.db_type = db_type
        self.fewshot_examples = FEWSHOT_EXAMPLES
        self.medical_terms = MEDICAL_TERMINOLOGY
        
    def build_instruction(self) -> str:
        """Build instruction section of prompt.
        
        Returns:
            Instruction text
        """
        return self.INSTRUCTION_TEMPLATE.format(db_type=self.db_type)
    
    def build_terminology_section(self) -> str:
        """Build medical terminology mapping section.
        
        Returns:
            Terminology mapping text
        """
        lines = ["医疗术语映射："]
        for chinese_term, english_terms in self.medical_terms.items():
            english_str = "、".join([f"'{term}'" for term in english_terms])
            lines.append(f"- \"{chinese_term}\" 对应诊断表中包含 {english_str} 的记录")
        return "\n".join(lines)
    
    def select_fewshot_examples(self, question: str, max_examples: int = 5) -> List[Dict]:
        """Select most relevant few-shot examples.
        
        Args:
            question: User's question
            max_examples: Maximum number of examples to return
            
        Returns:
            List of selected examples
        """
        # For now, return first N examples
        # In a more advanced version, we could use similarity matching
        return self.fewshot_examples[:max_examples]
    
    def build_fewshot_section(self, examples: List[Dict]) -> str:
        """Build few-shot examples section.
        
        Args:
            examples: List of example dictionaries
            
        Returns:
            Few-shot examples text
        """
        lines = ["以下是一些示例：\n"]
        
        for i, example in enumerate(examples, 1):
            lines.append(f"示例 {i}：")
            lines.append(f"问题：{example['question']}")
            lines.append(f"SQL：")
            lines.append(f"#{example['sql']}#")
            lines.append("")  # Empty line between examples
        
        return "\n".join(lines)
    
    def build_full_prompt(self, question: str, schema_text: str, 
                         max_examples: int = 5) -> str:
        """Build complete prompt for LLM.
        
        Args:
            question: User's natural language question
            schema_text: Formatted schema information
            max_examples: Maximum number of few-shot examples
            
        Returns:
            Complete prompt text
        """
        # 1. Instruction
        instruction = self.build_instruction()
        
        # 2. Schema context
        schema_section = "数据库结构信息：\n" + schema_text
        
        # 3. Time guidelines
        time_section = self.TIME_GUIDELINES
        
        # 4. Terminology
        terminology_section = self.build_terminology_section()
        
        # 5. Few-shot examples
        examples = self.select_fewshot_examples(question, max_examples)
        fewshot_section = self.build_fewshot_section(examples)
        
        # 6. User question
        question_section = f"""现在请处理以下问题：
问题：{question}

请只输出一条 SQL 查询，用 # 包裹，例如：
#SELECT ...#"""
        
        # Combine all sections
        prompt_parts = [
            instruction,
            schema_section,
            time_section,
            terminology_section,
            fewshot_section,
            question_section
        ]
        
        full_prompt = "\n\n".join(prompt_parts)
        
        logger.debug(f"Generated prompt length: {len(full_prompt)} characters")
        return full_prompt
    
    def add_fewshot_example(self, question: str, sql: str):
        """Add a new few-shot example.
        
        Args:
            question: Natural language question
            sql: Corresponding SQL query
        """
        self.fewshot_examples.append({
            "question": question,
            "sql": sql
        })
        logger.info(f"Added new few-shot example: {question}")
    
    def update_medical_terms(self, chinese_term: str, english_terms: List[str]):
        """Update medical terminology mapping.
        
        Args:
            chinese_term: Chinese medical term
            english_terms: List of corresponding English terms
        """
        self.medical_terms[chinese_term] = english_terms
        logger.info(f"Updated medical term mapping: {chinese_term}")
