# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive database security audit system for detecting and managing sensitive information across multiple database types (SQLite, MySQL, PostgreSQL). Features regex/keyword-based scanning, background task processing, JWT authentication, and RBAC.

## Development Commands

### Backend
```bash
cd backend
uv sync                    # Install dependencies
uv run python create_admin.py  # Create admin user
uv run python -m uvicorn app.main:app --reload  # Development server
```

### Frontend
```bash
cd frontend
npm install    # Install dependencies
npm run dev    # Development server (http://localhost:5173)
npm run build  # Production build
```

### Running the App
- Backend runs at http://localhost:8000
- API docs at http://localhost:8000/api/v1/docs
- Default credentials: admin/admin

## Architecture

### Backend (FastAPI)
- `app/api/` - REST endpoints
- `app/core/` - Security (JWT), configuration
- `app/db/` - SQLAlchemy models, async sessions
- `app/schemas/` - Pydantic request/response models
- `app/services/` - Business logic for scanning, users, roles

### Frontend (Vue 3)
- `src/views/` - Page components
- `src/stores/` - Pinia state management
- `src/router/` - Vue Router config
- `src/i18n.js` - Internationalization (EN/CN)

## Key Patterns

- Async SQLAlchemy with connection pooling per database type (aiosqlite, aiomysql, asyncpg)
- Background task processing for scans with real-time status via task ID polling
- JWT token-based authentication with role-based access control
- Frontend serves static files from backend (`app/public` symlink to `frontend/dist`)