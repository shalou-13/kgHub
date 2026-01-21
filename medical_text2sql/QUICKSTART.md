# 快速开始指南

## 5分钟快速体验

### 前提条件
- Python 3.8+
- PostgreSQL 或 MySQL 数据库
- OpenAI API Key（或兼容的 API）

### 步骤 1: 安装依赖
```bash
cd medical_text2sql
pip install -r requirements.txt
```

### 步骤 2: 配置环境
```bash
# 复制配置文件
cp .env.example .env

# 编辑配置（至少修改以下内容）
# DB_HOST=localhost
# DB_NAME=mimic_demo
# DB_USER=postgres
# DB_PASSWORD=your_password
# LLM_API_KEY=sk-your-api-key
```

### 步骤 3: 初始化数据库
```bash
# 创建数据库表和示例数据
python init_db.py

# 设置数据库元数据
python setup_schema.py
```

### 步骤 4: 运行演示
```bash
# 方式一：命令行交互
python demo.py

# 方式二：启动 Web 服务
python main.py
# 然后在浏览器打开: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

## 示例查询

在命令行或 Web 界面中尝试以下问题：

1. **简单统计**
   ```
   统计患者总数
   ```

2. **时间范围查询**
   ```
   查询2024年的住院记录数量
   ```

3. **条件筛选**
   ```
   统计糖尿病患者的平均年龄
   ```

4. **多表关联**
   ```
   查询住院时间最长的前10位患者
   ```

5. **聚合分析**
   ```
   统计男性和女性患者的住院次数
   ```

## Web API 使用

### 查询接口
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "统计糖尿病患者的平均年龄",
    "max_examples": 5
  }'
```

响应示例：
```json
{
  "success": true,
  "query_id": "20240121_120000_123456",
  "sql": "SELECT AVG(a.age) FROM admissions a...",
  "results": [{"avg_age": 45.5}],
  "result_count": 1
}
```

### 提交反馈
```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "20240121_120000_123456",
    "feedback": "correct"
  }'
```

### 查看统计
```bash
curl "http://localhost:8000/stats"
```

## 常见问题

### Q: 数据库连接失败
**A**: 检查 `.env` 中的数据库配置，确保数据库服务已启动。

### Q: LLM API 调用失败
**A**: 
1. 检查 API Key 是否正确
2. 确认网络可以访问 API 地址
3. 查看日志了解具体错误信息

### Q: 生成的 SQL 不准确
**A**: 
1. 在 `fewshot_data.py` 中添加更多相关示例
2. 确保数据库字段有准确的中文注释
3. 尝试使用更强的模型（如 GPT-4）

### Q: 如何添加新的示例
**A**: 编辑 `fewshot_data.py`，在 `FEWSHOT_EXAMPLES` 列表中添加：
```python
{
    "question": "你的问题",
    "sql": "对应的 SQL 查询"
}
```

## 下一步

- 📖 阅读完整文档：[README.md](README.md)
- 🏗️ 了解系统架构：[ARCHITECTURE.md](ARCHITECTURE.md)
- 🔧 根据实际需求调整配置和示例
- 📊 收集用户反馈，持续优化系统

## 技术支持

如有问题，请查看：
1. 项目 README
2. 架构文档
3. 代码注释
4. GitHub Issues
