"""Setup script to initialize schema with medical semantics and keywords."""
import logging
from sqlalchemy import create_engine
from config import config
from schema_manager import SchemaManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_schema_metadata():
    """Setup schema with medical semantics and keywords."""
    try:
        # Create engine
        engine = create_engine(config.database_url)
        
        # Initialize schema manager
        schema_manager = SchemaManager(engine)
        
        # Extract schema
        logger.info("Extracting schema from database...")
        schema_manager.extract_schema()
        
        # Add medical semantics for each table
        logger.info("Adding medical semantics...")
        
        # Patients table
        schema_manager.add_medical_semantics(
            "patients",
            comment="患者基本信息表",
            column_comments={
                "subject_id": "患者唯一标识符",
                "gender": "性别（M/F）",
                "dob": "出生日期",
                "dod": "死亡日期"
            }
        )
        schema_manager.set_table_keywords("patients", [
            "患者", "病人", "性别", "年龄", "出生", "死亡"
        ])
        
        # Admissions table
        schema_manager.add_medical_semantics(
            "admissions",
            comment="入院记录表",
            column_comments={
                "hadm_id": "住院唯一标识符",
                "subject_id": "患者ID",
                "admittime": "入院时间",
                "dischtime": "出院时间",
                "admission_type": "入院类型",
                "age": "入院时年龄"
            }
        )
        schema_manager.set_table_keywords("admissions", [
            "入院", "住院", "出院", "住院天数", "住院时间", "入院时间", "出院时间"
        ])
        
        # Diagnoses table
        schema_manager.add_medical_semantics(
            "diagnoses_icd",
            comment="诊断记录表（ICD编码）",
            column_comments={
                "row_id": "记录唯一标识",
                "subject_id": "患者ID",
                "hadm_id": "住院ID",
                "icd9_code": "ICD-9诊断代码",
                "seq_num": "诊断顺序",
                "long_title": "诊断名称"
            }
        )
        schema_manager.set_table_keywords("diagnoses_icd", [
            "诊断", "疾病", "ICD", "病种", "糖尿病", "高血压", "肺炎", "新冠"
        ])
        
        # Lab events table
        schema_manager.add_medical_semantics(
            "labevents",
            comment="化验检查结果表",
            column_comments={
                "row_id": "记录唯一标识",
                "subject_id": "患者ID",
                "hadm_id": "住院ID",
                "itemid": "检查项目ID",
                "charttime": "检查时间",
                "valuenum": "检查结果数值",
                "valueuom": "单位",
                "flag": "异常标记"
            }
        )
        schema_manager.set_table_keywords("labevents", [
            "化验", "检验", "实验室", "检查", "血糖", "血压", "结果"
        ])
        
        # Lab items dictionary
        schema_manager.add_medical_semantics(
            "d_labitems",
            comment="化验项目字典表",
            column_comments={
                "itemid": "项目ID",
                "label": "项目名称",
                "fluid": "样本类型",
                "category": "项目分类"
            }
        )
        schema_manager.set_table_keywords("d_labitems", [
            "化验项目", "检验项目", "项目"
        ])
        
        # ICU stays table
        schema_manager.add_medical_semantics(
            "icustays",
            comment="ICU住院记录表",
            column_comments={
                "icustay_id": "ICU住院唯一标识",
                "subject_id": "患者ID",
                "hadm_id": "住院ID",
                "intime": "ICU入院时间",
                "outtime": "ICU出院时间",
                "los": "ICU住院天数"
            }
        )
        schema_manager.set_table_keywords("icustays", [
            "ICU", "重症", "重症监护"
        ])
        
        # Save schema to file
        logger.info("Saving schema to file...")
        schema_manager.save_schema_to_file("medical_schema.json")
        
        logger.info("Schema setup completed successfully")
        
        # Display schema summary
        print("\n" + "="*80)
        print("数据库表结构概览:")
        print("="*80)
        for table_name in schema_manager.get_all_table_names():
            table_info = schema_manager.schema_cache[table_name]
            print(f"\n表名: {table_name}")
            print(f"说明: {table_info.get('comment', 'N/A')}")
            print(f"字段数: {len(table_info['columns'])}")
            if table_name in schema_manager.table_keywords:
                print(f"关键词: {', '.join(schema_manager.table_keywords[table_name])}")
        print("\n" + "="*80)
        
    except Exception as e:
        logger.error(f"Schema setup failed: {e}")
        raise


if __name__ == "__main__":
    setup_schema_metadata()
