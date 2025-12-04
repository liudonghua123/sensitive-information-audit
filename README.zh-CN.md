# 敏感信息审计系统

一个全面的数据库安全审计系统，用于检测和管理多种数据库类型中的敏感信息。

[English Documentation](./README.md)

## 功能特性

- 🔍 **多数据库支持**: 支持 SQLite, MySQL, PostgreSQL
- 🎯 **灵活的扫描规则**: 支持正则表达式和关键字匹配
- 🚀 **后台任务处理**: 带有实时状态更新的异步扫描
- 🔐 **安全认证**: 基于 JWT 的认证系统
- 👥 **基于角色的访问控制 (RBAC)**: 具有自定义角色的细粒度权限管理
- 👤 **用户管理**: 完整的用户管理功能
- 🌍 **国际化**: 支持中文和英文
- 🎨 **现代 UI**: 基于 Vue 3 和 Tailwind CSS 构建的美观、响应式界面

## 快速开始

### 先决条件

- Python 3.13+
- Node.js 18+
- `uv` (Python 包管理器)

### 安装

1. **克隆仓库**
   ```bash
   git clone https://github.com/liudonghua123/sensitive-information-audit.git
   cd sensitive-information-audit
   ```

2. **后端设置**
   ```bash
   cd backend
   
   # 安装依赖
   uv sync
   
   # 创建环境文件
   cp .env.example .env
   # 编辑 .env 并设置您的 SECRET_KEY
   
   # 创建管理员用户
   uv run python create_admin.py
   
   # 启动服务器
   uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **前端设置**
   ```bash
   cd frontend
   
   # 安装依赖
   npm install
   
   # 构建生产版本
   npm run build
   ```

4. **访问应用**
   
   打开浏览器并访问 `http://localhost:8000`
   
   默认凭据:
   - 用户名: `admin`
   - 密码: `admin`

## 项目结构

```
sensitive-information-audit/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 端点
│   │   ├── core/           # 核心功能 (安全, 配置)
│   │   ├── db/             # 数据库模型和会话
│   │   ├── schemas/        # Pydantic 模式
│   │   └── services/       # 业务逻辑
│   ├── create_admin.py     # 管理员用户创建脚本
│   └── pyproject.toml      # Python 依赖
└── frontend/               # Vue 3 前端
    ├── src/
    │   ├── views/          # 页面组件
    │   ├── stores/         # Pinia 状态管理
    │   ├── router/         # Vue Router 配置
    │   └── i18n.js         # 国际化
    └── package.json        # Node 依赖
```

## 开发

### 后端开发

```bash
cd backend
uv run python -m uvicorn app.main:app --reload
```

API 文档地址: `http://localhost:8000/api/v1/docs`

### 前端开发

```bash
cd frontend
npm run dev
```

开发服务器运行在 `http://localhost:5173`

## 使用指南

1. **添加数据库连接**: 配置要扫描的目标数据库
2. **定义扫描规则**: 创建基于正则或关键字的检测规则
3. **运行扫描**: 对选定的数据库执行后台扫描
4. **查看结果**: 审查检测到的敏感信息
5. **管理用户和角色**: 创建自定义角色并管理用户访问权限（仅限管理员）

## 技术栈

### 后端
- FastAPI
- SQLAlchemy (Async)
- Pydantic
- JWT Authentication
- Python 3.13+

### 前端
- Vue 3
- Tailwind CSS
- Pinia
- Vue Router
- Vue I18n

## 许可证

MIT

## 贡献

欢迎贡献！请随时提交 Pull Request。
