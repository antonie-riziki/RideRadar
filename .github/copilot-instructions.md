# RideRadar Copilot Instructions

## Project Overview
RideRadar is a **Django + React full-stack platform** for urban public transport (matatu/bus) commuters in Kenya. It provides:
- **Commuter app**: live vehicle tracking, route guidance, ticket management, AI chatbot
- **Admin dashboard**: fleet monitoring, analytics, route/fare management, AI recommendations
- **AI backend**: Google Gemini chatbot with transport intelligence for real-time alerts and trip guidance

## Architecture

### Backend (Django)
- **Stack**: Django 6.0, SQLite, Python 3.x
- **Entry point**: `manage.py runserver` (port 8000)
- **Key modules**:
  - `rideradar/settings.py`: Project config; includes `rideradar_app`
  - `rideradar_app/urls.py`: Routes for home, admin (dashboard/login/register/analytics/fleet-tracking/smart-recommendations), user (dashboard/login/register/live-tracking/tickets/trips), and chatbot
  - `rideradar_app/views.py`: Contains Gemini AI chatbot system instruction; renders templates; view endpoints TBD in models
  - `rideradar_app/templates/`: HTML templates for both commuter and admin UI

### Frontend (React + Vite)
- **Stack**: React 18, React Router v6, Vite 7
- **Dev**: `npm run dev` (port 3000) with auto-reload
- **Build**: `npm run build` outputs to `dist/`
- **API layer**: `src/api/api.js` handles all backend calls with fallback mock data; uses `VITE_API_BASE` env var (defaults to `http://localhost:8000/api`)
- **Component structure**:
  - `src/components/Commuter/`: Home, Map, Tickets
  - `src/components/Admin/`: Dashboard, Analytics
  - Routes: `/` (home), `/map`, `/tickets`, `/admin`

### Data Flow
1. Frontend (React) calls `src/api/api.js` helpers (e.g., `getVehicles()`)
2. API layer hits Django endpoints under `/api/` (not yet fully implemented)
3. Django views integrate Gemini AI for chatbot responses and recommendations
4. Mock fallbacks embedded in API layer ensure UI works offline

## Developer Workflows

### Setup
```bash
# Backend
python3 manage.py runserver

# Frontend (separate terminal)
cd frontend && npm run dev
```

### CORS Configuration (Dev)
Frontend (3000) → Backend (8000) requires CORS setup:
```python
# settings.py: add to INSTALLED_APPS and MIDDLEWARE
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

### Production Deployment
1. Build frontend: `npm run build` in `frontend/`
2. Copy `dist/` to Django static directory or set `STATICFILES_DIRS`
3. Run `python3 manage.py collectstatic`
4. Add SPA catch-all route to serve `index.html` for client-side routing

## Key Patterns & Conventions

### API Design
- **Endpoints**: Exposed under `/api/` (RESTful); examples in `api.js` include `/vehicles/`, `/tickets/`, `/overview/`, `/analytics/`
- **Auth**: Token/JWT expected for protected endpoints; frontend includes `Authorization: Bearer <token>` header when token provided
- **Fallbacks**: All `api.js` functions wrap calls in try-catch with mock data fallbacks (see `getVehicles()`, `getTickets()`, `getOverview()`)

### AI Chatbot (Gemini Integration)
- **System instruction**: Defined in `rideradar_app/views.py` as `GEMINI_SYSTEM_INSTRUCTION`
- **Scope**: Real-time alerts, route guidance, fleet intelligence, conversational support
- **Tone**: Calm, practical, human—not alarmist
- **Model**: Google Generative AI (genai library)
- **Endpoint**: `chatbot-response/` view (URL pattern in `urls.py`)

### UI Principles
- **Mobile-first** commuter experience (low cognitive load, single-purpose screens)
- **Web-first** admin dashboard (cards, maps, charts)
- **Design tokens**: Primary blue (#0b6e99), accent orange (#ff9f43)
- **Accessibility**: High contrast, large tap targets, color-blind safe
- **Internationalization**: English primary + optional Swahili

### Database & Models
- **Currently**: Empty `rideradar_app/models.py` (models TBD)
- **Storage**: SQLite (`db.sqlite3`)
- **Django admin**: Available at `/admin/` via Django's built-in admin site

## Critical Integration Points

### Chatbot Endpoint
- **URL**: `POST /chatbot-response/`
- **Integration**: Calls Google Gemini API with context; frontend submits messages here
- **Dependencies**: `google-genai`, `dotenv` (for API key in `.env`)

### Vehicle & Route Data
- **Live tracking**: API endpoints `/api/vehicles/`, `/api/routes/` (future WebSocket or polling)
- **Expected fields**: `id`, `route`, `lat`, `lon`, `direction`, `occupancy`, `eta_minutes`, `fare`
- **Front-end**: Real-time updates via polling or WebSocket (see `frontend_integration.md`)

### Environment Variables
- **Backend**: `.env` file (API keys for Gemini, Africa's Talking SMS)
- **Frontend**: `VITE_API_BASE` for API origin (dev: `http://localhost:8000/api`)

## Common Tasks

**Adding a new API endpoint**:
1. Create view in `rideradar_app/views.py`
2. Add route to `rideradar_app/urls.py`
3. Implement helper in `frontend/src/api/api.js` with mock fallback
4. Use in React component

**Updating the chatbot**:
- Modify `GEMINI_SYSTEM_INSTRUCTION` in `views.py`
- Test via `POST /chatbot-response/` (send JSON with user message)

**Deploying frontend**:
- `npm run build` and serve from Django static files or separate web server
- Ensure API_BASE env var points to correct Django API URL

## File Reference
- Backend logic: [rideradar_app/views.py](../rideradar_app/views.py), [rideradar_app/urls.py](../rideradar_app/urls.py)
- Frontend routes: [frontend/src/App.jsx](../frontend/src/App.jsx), [frontend/src/api/api.js](../frontend/src/api/api.js)
- Docs: [frontend/docs/frontend_integration.md](../frontend/docs/frontend_integration.md), [frontend/docs/UX_ARCHITECTURE.md](../frontend/docs/UX_ARCHITECTURE.md)
- Config: [rideradar/settings.py](../rideradar/settings.py), [frontend/vite.config.js](../frontend/vite.config.js)
