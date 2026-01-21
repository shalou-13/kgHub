"""Command-line demo for medical Text-to-SQL system."""
import logging
from sqlalchemy import create_engine

from config import config
from schema_manager import SchemaManager
from prompt_builder import PromptBuilder
from llm_client import Text2SQLConverter
from sql_executor import SQLSecurityFilter, SQLExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run command-line demo."""
    print("="*80)
    print("医疗 Text-to-SQL 系统 - 命令行演示")
    print("="*80)
    print()
    
    try:
        # Initialize components
        print("初始化系统组件...")
        
        # Database connection
        engine = create_engine(config.database_url)
        
        # Schema manager
        schema_manager = SchemaManager(engine)
        try:
            schema_manager.load_schema_from_file("medical_schema.json")
            print("✓ 从文件加载数据库结构")
        except FileNotFoundError:
            print("! 未找到结构文件，从数据库提取...")
            schema_manager.extract_schema()
            schema_manager.save_schema_to_file("medical_schema.json")
        
        # Prompt builder
        prompt_builder = PromptBuilder(db_type=config.DB_TYPE)
        print("✓ 初始化 Prompt 构造器")
        
        # LLM converter
        llm_converter = Text2SQLConverter()
        print("✓ 初始化 LLM 转换器")
        
        # SQL executor
        allowed_tables = schema_manager.get_all_table_names()
        security_filter = SQLSecurityFilter(allowed_tables)
        sql_executor = SQLExecutor(engine, security_filter)
        print("✓ 初始化 SQL 执行器")
        
        print()
        print("系统初始化完成！")
        print()
        print("可用的数据库表：")
        for table_name in allowed_tables:
            table_info = schema_manager.schema_cache.get(table_name, {})
            comment = table_info.get("comment", "")
            print(f"  - {table_name}: {comment}")
        
        print()
        print("="*80)
        print()
        
        # Interactive query loop
        while True:
            print("请输入您的问题（输入 'quit' 或 'exit' 退出）：")
            question = input("> ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("感谢使用！再见！")
                break
            
            if not question:
                continue
            
            print()
            print("-"*80)
            print(f"问题: {question}")
            print("-"*80)
            
            try:
                # Select relevant tables
                relevant_tables = schema_manager.select_relevant_tables(question)
                print(f"相关表: {', '.join(relevant_tables)}")
                
                # Render schema
                schema_text = schema_manager.render_schema_text(relevant_tables)
                
                # Build prompt
                prompt = prompt_builder.build_full_prompt(question, schema_text, max_examples=3)
                
                print("生成 SQL 查询中...")
                
                # Convert to SQL
                sql = llm_converter.convert(prompt)
                
                if not sql:
                    print("✗ 无法生成 SQL 查询")
                    print()
                    continue
                
                print(f"\n生成的 SQL:")
                print("-"*80)
                print(sql)
                print("-"*80)
                
                # Execute SQL
                print("\n执行查询...")
                success, results, error = sql_executor.execute_query(sql)
                
                if success:
                    print(f"✓ 查询成功！返回 {len(results)} 条结果")
                    
                    if results:
                        print("\n查询结果（前10条）:")
                        print("-"*80)
                        
                        # Print header
                        if results:
                            headers = list(results[0].keys())
                            header_line = " | ".join([f"{h:20s}" for h in headers])
                            print(header_line)
                            print("-"*80)
                            
                            # Print rows (max 10)
                            for row in results[:10]:
                                row_line = " | ".join([f"{str(row[h])[:20]:20s}" for h in headers])
                                print(row_line)
                    else:
                        print("查询结果为空")
                else:
                    print(f"✗ 查询失败: {error}")
                
            except Exception as e:
                print(f"✗ 处理过程出错: {e}")
                logger.error(f"Error processing question: {e}", exc_info=True)
            
            print()
            print("="*80)
            print()
    
    except Exception as e:
        print(f"\n系统初始化失败: {e}")
        logger.error(f"System initialization failed: {e}", exc_info=True)
        return


if __name__ == "__main__":
    main()
