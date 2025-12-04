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
   uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **Package an executable**
   ```bash
   pyinstaller main.py --onefile --name sensitive-information-audit.exe --add-data "app;app" --hidden-import uvicorn --hidden-import aiosqlite --hidden-import bcrypt --hidden-import passlib.handlers.bcrypt --paths "/full/path/to/.venv/Lib/site-packages"
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
- `SECRET_KEY`: JWT secret key (change in production!)
- `DATABASE_URL`: Application database URL
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development

### Running with auto-reload
```bash
uv run python -m uvicorn app.main:app --reload
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
