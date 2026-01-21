# 医疗 Text-to-SQL 系统

基于 LLM + Prompt Engineering 的医疗数据库自然语言查询系统

## 项目概述

本系统将用户的中文自然语言问题转换为 SQL 查询，专门针对医疗数据库（MIMIC-III 简化版）设计。系统采用 Prompt Engineering 技术，结合数据库结构信息、Few-shot 示例和医疗术语映射，实现准确的 SQL 生成。

### 主要特性

- 🏥 **医疗领域专用**: 针对医疗数据库优化，支持常见医疗查询场景
- 🔒 **安全过滤**: 内置 SQL 安全检查，防止危险操作
- 🎯 **智能检索**: 自动选择相关数据库表，优化 Prompt 效率
- 🔄 **错误重试**: 查询失败时自动重试和修正
- 📊 **反馈收集**: 记录查询历史和用户反馈，支持持续优化
- 🌐 **Web API**: 基于 FastAPI 的 RESTful API 接口

## 技术栈

- **后端框架**: FastAPI
- **数据库**: PostgreSQL / MySQL（支持两者）
- **ORM**: SQLAlchemy
- **LLM**: OpenAI API（兼容其他 OpenAI 格式 API）
- **中文分词**: jieba

## 系统架构

```
┌─────────────────┐
│  用户自然语言问题  │
└────────┬────────┘
         ↓
┌────────────────────┐
│  Schema 检索模块    │ ← 选择相关数据库表
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Prompt 构造模块    │ ← 拼接完整 Prompt
└────────┬───────────┘
         ↓
┌────────────────────┐
│   LLM 调用模块      │ ← 调用大模型生成 SQL
└────────┬───────────┘
         ↓
┌────────────────────┐
│  SQL 安全过滤模块   │ ← 验证 SQL 安全性
└────────┬───────────┘
         ↓
┌────────────────────┐
│  SQL 执行模块       │ ← 执行查询并返回结果
└────────┬───────────┘
         ↓
┌────────────────────┐
│  反馈收集模块       │ ← 记录查询日志和反馈
└────────────────────┘
```

## 安装部署

### 1. 环境要求

- Python 3.8+
- PostgreSQL 或 MySQL 数据库
- LLM API 访问权限（OpenAI 或兼容接口）

### 2. 安装依赖

```bash
cd medical_text2sql
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置
DB_TYPE=postgresql  # 或 mysql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mimic_demo
DB_USER=postgres
DB_PASSWORD=your_password

# LLM API 配置
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key
LLM_API_BASE=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo

# 应用配置
MAX_RESULT_ROWS=1000
ENABLE_SQL_RETRY=true
MAX_RETRY_COUNT=2
LOG_LEVEL=INFO
```

### 4. 初始化数据库

```bash
# 创建数据库表和示例数据
python init_db.py

# 设置数据库结构元数据
python setup_schema.py
```

## 使用方法

### 方式一：命令行演示

```bash
python demo.py
```

交互式命令行界面，输入问题即可查询：

```
请输入您的问题（输入 'quit' 或 'exit' 退出）：
> 统计2024年住院超过7天的成年患者人数

生成的 SQL:
SELECT COUNT(DISTINCT a.hadm_id)
FROM admissions a
WHERE a.admittime >= '2024-01-01'
  AND a.admittime < '2025-01-01'
  AND EXTRACT(DAY FROM (a.dischtime - a.admittime)) > 7
  AND a.age >= 18;

✓ 查询成功！返回 1 条结果
```

### 方式二：Web API 服务

启动 FastAPI 服务：

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 API 文档：http://localhost:8000/docs

#### API 端点

1. **查询接口** `POST /query`

请求示例：
```json
{
  "question": "统计糖尿病患者的平均年龄",
  "max_examples": 5
}
```

响应示例：
```json
{
  "success": true,
  "query_id": "20240101_120000_123456",
  "sql": "SELECT AVG(a.age) as avg_age FROM admissions a INNER JOIN diagnoses_icd d ON a.hadm_id = d.hadm_id WHERE d.long_title LIKE '%diabetes%';",
  "results": [{"avg_age": 45.5}],
  "result_count": 1
}
```

2. **反馈接口** `POST /feedback`

```json
{
  "query_id": "20240101_120000_123456",
  "feedback": "correct",
  "corrected_sql": null
}
```

3. **统计接口** `GET /stats`

返回查询和反馈统计信息。

4. **健康检查** `GET /health`

## 数据库结构

系统使用简化的 MIMIC-III 数据库结构：

| 表名 | 说明 | 主要字段 |
|------|------|---------|
| patients | 患者基本信息 | subject_id, gender, dob, dod |
| admissions | 入院记录 | hadm_id, subject_id, admittime, dischtime, age |
| diagnoses_icd | 诊断记录 | subject_id, hadm_id, icd9_code, long_title |
| labevents | 化验检查结果 | subject_id, hadm_id, itemid, charttime, valuenum |
| d_labitems | 化验项目字典 | itemid, label, fluid, category |
| icustays | ICU住院记录 | icustay_id, subject_id, hadm_id, intime, outtime |

## 示例查询

系统支持的典型查询类型：

1. **统计查询**
   - "统计2024年住院超过7天的成年患者人数"
   - "统计糖尿病患者的平均年龄"
   - "统计每种诊断类型的患者数量"

2. **时间范围查询**
   - "查询最近30天内有新冠肺炎诊断的患者数量"
   - "查询2024年1月的所有入院记录"

3. **多表关联查询**
   - "查询住院时间最长的前10位患者的基本信息"
   - "查询血糖检验结果异常的患者记录"

4. **聚合分析**
   - "统计男性和女性患者的住院次数"
   - "查询在ICU住院的患者平均住院天数"

## 核心模块说明

### 1. Schema Manager (schema_manager.py)
- 从数据库提取结构信息
- 管理医疗语义标注
- 基于规则的相关表检索

### 2. Prompt Builder (prompt_builder.py)
- 构建完整 Prompt
- 管理 Few-shot 示例
- 医疗术语映射

### 3. LLM Client (llm_client.py)
- 调用各类 LLM API
- 从响应中提取 SQL
- SQL 清洗和规范化

### 4. SQL Executor (sql_executor.py)
- SQL 安全过滤（黑名单、白名单）
- 查询执行和结果返回
- 错误重试机制

### 5. Feedback Collector (feedback.py)
- 查询日志记录
- 用户反馈收集
- 训练数据导出

## 安全特性

1. **黑名单过滤**: 拒绝 DDL/DML 操作（DROP, DELETE, INSERT, UPDATE 等）
2. **表访问控制**: 仅允许访问白名单中的表
3. **结果行数限制**: 自动添加 LIMIT 子句，防止返回过多数据
4. **错误信息脱敏**: 隐藏敏感的错误详情

## 持续优化

系统支持基于反馈的持续改进：

1. **收集反馈**: 用户对每次查询结果打标签（正确/部分正确/错误）
2. **人工修正**: 对错误的 SQL 进行人工修正
3. **导出训练数据**: 将高质量样本导出为新的 Few-shot 示例
4. **定期更新**: 用优质样本更新 Prompt 中的示例集

```bash
# 从反馈日志导出训练数据
python -c "
from feedback import FeedbackCollector
fc = FeedbackCollector('data/feedback_log.jsonl')
fc.export_training_data('training_data.json', feedback_filter=['correct', 'partial'])
"
```

## 扩展指南

### 添加新的 Few-shot 示例

编辑 `fewshot_data.py`，在 `FEWSHOT_EXAMPLES` 列表中添加：

```python
{
    "question": "您的问题",
    "sql": "SELECT ... FROM ... WHERE ..."
}
```

### 添加医疗术语映射

编辑 `fewshot_data.py`，在 `MEDICAL_TERMINOLOGY` 字典中添加：

```python
"中文术语": ["english_term1", "english_term2"]
```

### 支持新的 LLM Provider

在 `llm_client.py` 的 `LLMClient` 类中添加新的调用方法。

## 故障排除

### 1. 数据库连接失败
- 检查 `.env` 中的数据库配置
- 确认数据库服务已启动
- 验证用户权限

### 2. LLM API 调用失败
- 检查 API Key 是否正确
- 确认 API Base URL 可访问
- 查看网络连接和代理设置

### 3. SQL 生成质量差
- 增加相关的 Few-shot 示例
- 优化数据库字段注释
- 调整 Prompt 模板
- 考虑使用更强的模型

## 项目结构

```
medical_text2sql/
├── README.md                 # 项目文档
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量示例
├── config.py                # 配置管理
├── database_schema.py       # 数据库结构定义
├── init_db.py              # 数据库初始化脚本
├── setup_schema.py         # 结构元数据设置
├── schema_manager.py       # 结构管理模块
├── fewshot_data.py         # Few-shot 示例数据
├── prompt_builder.py       # Prompt 构造模块
├── llm_client.py          # LLM 调用模块
├── sql_executor.py        # SQL 执行模块
├── feedback.py            # 反馈收集模块
├── main.py               # FastAPI Web 服务
└── demo.py               # 命令行演示程序
```

## 开发路线图

- [x] 第0步：本地 Demo 实现
- [x] 第1步：Web 服务化
- [x] 第2步：Schema 检索 + 安全过滤
- [x] 第3步：反馈收集机制
- [ ] 第4步：向量检索优化
- [ ] 第5步：多轮对话支持
- [ ] 第6步：模型微调

## 参考资料

本项目基于以下技术和最佳实践：

1. MIMIC-III 数据库结构
2. Text-to-SQL 任务最佳实践
3. LLM Prompt Engineering 技术
4. 医疗信息系统安全标准

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
