# Frontend - Sensitive Information Audit System

Vue 3 frontend for the Sensitive Information Audit System.

## Features

- Modern, responsive UI with Tailwind CSS
- Internationalization (i18n) support
- State management with Pinia
- JWT authentication
- Real-time task monitoring

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Development server**
   ```bash
   npm run dev
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## Project Structure

```
frontend/
├── src/
│   ├── views/              # Page components
│   │   ├── Login.vue       # Login page
│   │   ├── Dashboard.vue   # Main layout
│   │   ├── Connections.vue # Database connections
│   │   ├── Rules.vue       # Scan rules
│   │   └── Tasks.vue       # Task monitoring
│   ├── stores/             # Pinia stores
│   │   └── auth.js         # Authentication store
│   ├── router/             # Vue Router
│   │   └── index.js        # Route configuration
│   ├── api.js              # Axios instance
│   ├── i18n.js             # Internationalization
│   ├── style.css           # Global styles
│   ├── App.vue             # Root component
│   └── main.js             # Application entry
├── public/                 # Static assets
├── index.html              # HTML template
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS configuration
└── vite.config.js          # Vite configuration
```

## Internationalization

The application supports multiple languages:
- English (en-US)
- Chinese (zh-CN)

Language can be switched from the Connections page. The selection is persisted in localStorage.

### Adding a new language

1. Edit `src/i18n.js`
2. Add translations to the `messages` object
3. Update the language selector in components

## Features

### Database Connections
- Add, view, and delete database connections
- Test connection before saving
- Support for SQLite, MySQL, PostgreSQL

### Scan Rules
- Create custom regex or keyword rules
- View system and user-defined rules
- Delete user rules

### Tasks & Results
- Start background scans
- Monitor task status in real-time
- View detailed scan results

## Development

### API Configuration

The frontend connects to the backend API at `http://localhost:8000/api/v1` by default.

To change this, edit `src/api.js`:
```javascript
const api = axios.create({
  baseURL: 'http://your-api-url/api/v1',
});
```

### Styling

The project uses Tailwind CSS with custom configuration:
- Custom color palette (primary, secondary)
- Inter font family
- Custom utility classes (btn-primary, input-field, etc.)

## Build

The production build is served by the backend at `http://localhost:8000`.

To build:
```bash
npm run build
```

The output will be in the `dist/` directory, which is served by the FastAPI backend.

## Dependencies

- `vue`: Frontend framework
- `vue-router`: Routing
- `pinia`: State management
- `vue-i18n`: Internationalization
- `axios`: HTTP client
- `tailwindcss`: Utility-first CSS
- `vite`: Build tool
