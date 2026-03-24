# Backend - Sensitive Information Audit System

FastAPI-based backend for the Sensitive Information Audit System.

## Features

- RESTful API with FastAPI
- Async database operations with SQLAlchemy
- JWT-based authentication
- Background task processing
- Multi-database connector (SQLite, MySQL, PostgreSQL)

## Setup

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

3. **Create admin user**
   ```bash
   uv run python create_admin.py
   ```

4. **Run the server**
   ```bash
   uv run python main.py
   ```
   The server will start and automatically open your browser at `http://localhost:8000`.

   You can customize the host and port:
   ```bash
   HOST=0.0.0.0 PORT=8080 uv run python main.py
   ```

   Or configure them in `.env`:
   ```
   HOST=0.0.0.0
   PORT=8000
   ```

5. **Package an executable**
   ```bash
   pyinstaller sensitive-information-audit.exe.spec
   ```
   The executable will be created in the `dist` folder.

   To build from scratch with all required hidden imports:
   ```bash
   pyinstaller main.py --onefile --name sensitive-information-audit.exe \
     --add-data "app;app" \
     --hidden-import fastapi \
     --hidden-import uvicorn \
     --hidden-import uvicorn.logging \
     --hidden-import uvicorn.loops \
     --hidden-import uvicorn.loops.auto \
     --hidden-import uvicorn.protocols \
     --hidden-import uvicorn.protocols.http \
     --hidden-import uvicorn.protocols.http.h11 \
     --hidden-import uvicorn.protocols.websockets \
     --hidden-import uvicorn.protocols.websockets.auto \
     --hidden-import uvicorn.lifespan \
     --hidden-import uvicorn.lifespan.on \
     --hidden-import starlette \
     --hidden-import starlette.responses \
     --hidden-import starlette.routing \
     --hidden-import starlette.middleware \
     --hidden-import starlette.middleware.cors \
     --hidden-import starlette.staticfiles \
     --hidden-import sqlalchemy \
     --hidden-import sqlalchemy.ext \
     --hidden-import sqlalchemy.ext.asyncio \
     --hidden-import aiosqlite \
     --hidden-import aiomysql \
     --hidden-import asyncpg \
     --hidden-import bcrypt \
     --hidden-import passlib \
     --hidden-import passlib.handlers \
     --hidden-import passlib.handlers.bcrypt \
     --hidden-import pydantic \
     --hidden-import pydantic_settings \
     --hidden-import python_jose \
     --hidden-import python_jose.cryptography \
     --hidden-import cryptography \
     --hidden-import python_multipart \
     --hidden-import docx \
     --hidden-import reportlab \
     --paths ".venv/Lib/site-packages"
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/                # API routes
│   │   └── api_v1/
│   │       ├── endpoints/  # Endpoint handlers
│   │       └── api.py      # API router
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration
│   │   └── security.py     # Authentication & security
│   ├── db/                 # Database
│   │   ├── models.py       # SQLAlchemy models
│   │   └── session.py      # Database session
│   ├── schemas/            # Pydantic schemas
│   │   └── all.py          # Request/response models
│   ├── services/           # Business logic
│   │   ├── connector.py    # Database connector
│   │   └── scanner.py      # Scanning service
│   └── main.py             # Application entry point
├── create_admin.py         # Admin user creation script
├── main.py                 # Development runner
├── pyproject.toml          # Dependencies
└── .env.example            # Environment template
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 8000)
- `SECRET_KEY`: JWT secret key (change in production!)
- `DATABASE_URL`: Application database URL
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development

The development server auto-reloads on code changes:
```bash
uv run python main.py
```

### Database migrations
The application automatically creates tables on startup. To reset:
```bash
# Delete the database file
rm audit.db
# Restart the server to recreate tables
```

## Testing Database Connections

The API provides a `/connections/test` endpoint to verify database connectivity before saving.

## Dependencies

- `fastapi`: Web framework
- `sqlalchemy`: ORM with async support
- `pydantic`: Data validation
- `python-jose`: JWT handling
- `passlib`: Password hashing
- `uvicorn`: ASGI server
- `aiomysql`, `asyncpg`, `aiosqlite`: Database drivers
