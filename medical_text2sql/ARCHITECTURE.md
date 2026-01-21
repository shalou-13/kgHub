# 医疗 Text-to-SQL 系统架构文档

## 系统概述

本系统实现了一个基于 LLM + Prompt Engineering 的医疗领域自然语言到 SQL 转换系统，遵循问题陈述中的算法实现蓝图。

## 模块架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户接口层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Web API     │  │  CLI Demo    │  │  Web UI      │     │
│  │  (main.py)   │  │  (demo.py)   │  │(index.html)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      核心处理层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Schema       │  │ Prompt       │  │ LLM          │     │
│  │ Manager      │→ │ Builder      │→ │ Client       │     │
│  │ (检索相关表)  │  │ (构造提示词)  │  │ (生成SQL)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      安全执行层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ SQL Security │→ │ SQL          │→ │ Feedback     │     │
│  │ Filter       │  │ Executor     │  │ Collector    │     │
│  │ (安全检查)    │  │ (执行查询)    │  │ (记录反馈)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据存储层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Medical      │  │ Schema       │  │ Feedback     │     │
│  │ Database     │  │ Cache        │  │ Logs         │     │
│  │ (医疗数据库)  │  │ (结构缓存)    │  │ (反馈日志)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 核心模块详解

### 1. Schema Manager (schema_manager.py)
**职责**: 数据库结构管理与检索

**功能**:
- 从数据库提取表结构信息
- 添加医疗领域语义标注
- 基于关键词匹配选择相关表
- 将结构信息渲染为 Prompt 文本

**关键方法**:
```python
extract_schema()              # 从数据库提取结构
add_medical_semantics()       # 添加医疗语义
set_table_keywords()          # 设置表关键词
select_relevant_tables()      # 选择相关表
render_schema_text()          # 渲染为文本
```

### 2. Prompt Builder (prompt_builder.py)
**职责**: 构造完整的 LLM Prompt

**Prompt 结构** (按顺序):
1. **Instruction**: 任务说明和约束
2. **Schema Context**: 相关数据库表结构
3. **Time Guidelines**: 时间表达式规范
4. **Terminology**: 医疗术语映射
5. **Few-shot Examples**: 示例问题和 SQL
6. **User Question**: 用户的实际问题

**关键方法**:
```python
build_instruction()           # 构造指令部分
build_terminology_section()   # 构造术语映射
select_fewshot_examples()     # 选择示例
build_full_prompt()           # 构造完整 Prompt
```

### 3. LLM Client (llm_client.py)
**职责**: 调用 LLM API 并提取 SQL

**支持的 LLM**:
- OpenAI API
- 其他 OpenAI 兼容 API（通义、讯飞等）

**SQL 提取策略** (优先级顺序):
1. 提取 `#...#` 标记之间的内容
2. 提取 \`\`\`sql...\`\`\` 代码块
3. 提取 SELECT 语句模式
4. 返回完整响应

**关键方法**:
```python
call_llm()                    # 调用 LLM
extract_sql()                 # 提取 SQL
clean_sql()                   # 清理规范化
```

### 4. SQL Executor (sql_executor.py)
**职责**: SQL 安全检查与执行

**安全机制**:
1. **黑名单检查**: 拒绝 DDL/DML 操作
   - DROP, DELETE, INSERT, UPDATE, ALTER, CREATE 等
2. **白名单检查**: 仅允许访问指定表
3. **结果限制**: 自动添加 LIMIT 子句
4. **错误重试**: 失败时请求 LLM 修正

**关键方法**:
```python
validate_and_sanitize()       # 验证并净化 SQL
execute_query()               # 执行查询
execute_with_retry()          # 带重试的执行
```

### 5. Feedback Collector (feedback.py)
**职责**: 收集查询日志和用户反馈

**记录信息**:
- 查询ID和时间戳
- 原始问题和生成的 SQL
- 执行成功/失败状态
- 用户反馈（正确/部分正确/错误）
- 人工修正的 SQL

**关键方法**:
```python
log_query()                   # 记录查询
add_feedback()                # 添加反馈
get_feedback_stats()          # 获取统计
export_training_data()        # 导出训练数据
```

## 数据流程

### 标准查询流程
```
1. 接收问题 → "统计糖尿病患者的平均年龄"
2. 选择相关表 → [admissions, diagnoses_icd]
3. 渲染结构 → "表 admissions: subject_id, age..."
4. 构造 Prompt → 指令 + 结构 + 示例 + 问题
5. 调用 LLM → 生成响应
6. 提取 SQL → "SELECT AVG(a.age)..."
7. 安全检查 → 通过
8. 执行查询 → 返回结果
9. 记录日志 → 保存到 feedback_log.jsonl
```

### 错误重试流程
```
1. 执行失败 → 语法错误或字段不存在
2. 构造重试 Prompt → 包含错误信息
3. 调用 LLM → 生成修正后的 SQL
4. 再次执行 → 成功或达到最大重试次数
```

## 配置说明

### 环境变量 (.env)
```
DB_TYPE         # 数据库类型 (postgresql/mysql)
DB_HOST         # 数据库主机
DB_PORT         # 数据库端口
DB_NAME         # 数据库名称
DB_USER         # 数据库用户
DB_PASSWORD     # 数据库密码

LLM_PROVIDER    # LLM 提供商 (openai/tongyi/xunfei)
LLM_API_KEY     # API 密钥
LLM_API_BASE    # API 基础 URL
LLM_MODEL       # 模型名称

MAX_RESULT_ROWS # 最大返回行数 (默认 1000)
ENABLE_SQL_RETRY # 是否启用重试 (默认 true)
MAX_RETRY_COUNT # 最大重试次数 (默认 2)
LOG_LEVEL       # 日志级别 (默认 INFO)
```

## 部署步骤

### 开发环境部署
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
vim .env  # 修改配置

# 3. 初始化数据库
python init_db.py
python setup_schema.py

# 4. 运行演示
python demo.py

# 或启动 Web 服务
python main.py
```

### 生产环境部署
```bash
# 使用 Gunicorn 运行
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# 或使用 Docker
docker build -t medical-text2sql .
docker run -p 8000:8000 --env-file .env medical-text2sql
```

## 性能优化建议

1. **Schema 缓存**: 使用文件缓存避免频繁查询数据库结构
2. **表检索优化**: 考虑使用向量检索替代关键词匹配
3. **Prompt 优化**: 根据反馈数据定期更新 Few-shot 示例
4. **并发控制**: 使用连接池管理数据库连接
5. **缓存策略**: 对相同问题缓存 SQL 结果

## 安全考虑

1. ✅ SQL 注入防护 - 使用参数化查询和黑名单
2. ✅ 权限控制 - 仅允许 SELECT 查询
3. ✅ 资源限制 - 限制返回行数
4. ✅ 错误脱敏 - 隐藏敏感错误信息
5. ⚠️ API 认证 - 建议在生产环境添加
6. ⚠️ 速率限制 - 建议添加防滥用机制

## 扩展路线图

### 已实现 ✅
- [x] 基础 Text-to-SQL 转换
- [x] Web API 服务
- [x] 命令行界面
- [x] 安全过滤机制
- [x] 反馈收集系统

### 计划中 📋
- [ ] 向量检索优化（使用 Embedding）
- [ ] 多轮对话支持
- [ ] SQL 执行计划分析
- [ ] 查询结果可视化
- [ ] 模型微调支持
- [ ] 缓存机制
- [ ] 用户认证系统
- [ ] 管理后台界面

## 测试建议

### 单元测试
```python
# 测试 Schema Manager
def test_select_relevant_tables():
    manager = SchemaManager(engine)
    tables = manager.select_relevant_tables("统计糖尿病患者")
    assert "diagnoses_icd" in tables
    assert "admissions" in tables

# 测试 SQL 安全过滤
def test_security_filter():
    filter = SQLSecurityFilter(["admissions"])
    is_safe, _ = filter.check_blacklist("DROP TABLE admissions")
    assert not is_safe
```

### 集成测试
```python
# 端到端测试
def test_full_query_pipeline():
    response = client.post("/query", json={
        "question": "统计患者总数"
    })
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## 监控指标

建议监控的关键指标：

1. **查询成功率**: 成功查询 / 总查询数
2. **平均响应时间**: LLM 调用 + SQL 执行时间
3. **SQL 准确率**: 基于用户反馈计算
4. **重试率**: 需要重试的查询比例
5. **错误类型分布**: 统计常见错误原因

## 参考资料

- 问题陈述文档 - 算法实现蓝图
- MIMIC-III 数据库文档
- FastAPI 官方文档
- SQLAlchemy 文档
- OpenAI API 文档
