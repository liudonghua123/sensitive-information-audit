# Sensitive Information Audit System

A comprehensive database security audit system for detecting and managing sensitive information across multiple database types.

[中文文档](./README.zh-CN.md)

## Features

- 🔍 **Multi-Database Support**: SQLite, MySQL, PostgreSQL
- 🎯 **Flexible Scanning Rules**: Regex patterns and keyword matching
- 🚀 **Background Task Processing**: Asynchronous scanning with real-time status updates
- 🔐 **Secure Authentication**: JWT-based authentication system
- 👥 **Role-Based Access Control (RBAC)**: Granular permission management with custom roles
- 👤 **User Management**: Full user administration capabilities
- 🌍 **Internationalization**: Support for English and Chinese
- 🎨 **Modern UI**: Beautiful, responsive interface built with Vue 3 and Tailwind CSS

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- `uv` (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/liudonghua123/sensitive-information-audit.git
   cd sensitive-information-audit
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Install dependencies
   uv sync
   
   # Create environment file
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   
   # Create admin user
   uv run python create_admin.py

   # Start the server (opens browser automatically)
   cd backend && uv run python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Build for production
   npm run build
   ```

4. **Access the Application**
   
   Open your browser and navigate to `http://localhost:8000`
   
   Default credentials:
   - Username: `admin`
   - Password: `admin`

## Project Structure

```
sensitive-information-audit/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality (security, config)
│   │   ├── db/             # Database models and session
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── create_admin.py     # Admin user creation script
│   └── pyproject.toml      # Python dependencies
└── frontend/               # Vue 3 frontend
    ├── src/
    │   ├── views/          # Page components
    │   ├── stores/         # Pinia state management
    │   ├── router/         # Vue Router configuration
    │   └── i18n.js         # Internationalization
    └── package.json        # Node dependencies
```

## Development

### Backend Development

```bash
cd backend
uv run python main.py
```

API documentation available at `http://localhost:8000/api/v1/docs`

### Frontend Development

```bash
cd frontend
npm run dev
```

Development server runs at `http://localhost:5173`

## Usage

1. **Add Database Connections**: Configure target databases for scanning
2. **Define Scan Rules**: Create regex or keyword-based detection rules
3. **Run Scans**: Execute background scans on selected databases
4. **View Results**: Review detected sensitive information
5. **Manage Users & Roles**: Create custom roles and manage user access (Admin only)

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy (Async)
- Pydantic
- JWT Authentication
- Python 3.13+

### Frontend
- Vue 3
- Tailwind CSS
- Pinia
- Vue Router
- Vue I18n

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
