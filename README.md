# kgHub
knowledge graphs management

## 新增项目：医疗 Text-to-SQL 系统

本仓库新增了一个基于 LLM + Prompt Engineering 的医疗 Text-to-SQL 系统。该系统可以将自然语言问题转换为 SQL 查询，专门针对医疗数据库设计。

### 项目位置
- 📂 `medical_text2sql/` - 医疗 Text-to-SQL 系统完整实现

### 主要特性
- 🏥 医疗领域专用的自然语言到SQL转换
- 🔒 内置安全过滤机制，防止危险SQL操作
- 🎯 智能表检索，自动选择相关数据库表
- 🔄 支持SQL错误重试和自动修正
- 📊 完整的反馈收集和日志系统
- 🌐 FastAPI Web API + 简单前端界面

### 快速开始

1. 进入项目目录：
```bash
cd medical_text2sql
```

2. 查看详细文档：
```bash
cat README.md
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量（参考 `.env.example`）

5. 初始化数据库：
```bash
python init_db.py
python setup_schema.py
```

6. 运行演示：
```bash
# 命令行演示
python demo.py

# 或启动Web服务
python main.py
```

### 技术栈
- Python + FastAPI
- SQLAlchemy (支持 PostgreSQL/MySQL)
- OpenAI API (或兼容接口)
- jieba 中文分词

详细文档请参考：[medical_text2sql/README.md](medical_text2sql/README.md)
