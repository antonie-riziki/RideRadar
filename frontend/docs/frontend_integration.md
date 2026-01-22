# Frontend ↔ Django Integration Guide

This document explains how to run the React frontend with the existing Django backend and how to serve the built frontend in production.

Dev setup (recommended):
- Run Django normally (`python3 manage.py runserver` on port 8000).
- Start React dev server for frontend (`npm run dev` in `frontend/`) on port 3000.
- Configure the Django API to accept requests from the dev origin.

CORS (dev):
1. Install `django-cors-headers` in the backend:

```bash
pip install django-cors-headers
```

2. In `settings.py`, add:

```py
INSTALLED_APPS += [ 'corsheaders' ]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

API endpoints:
- Expose RESTful endpoints under `/api/` (use Django REST Framework recommended).
- Use token/JWT auth for protected endpoints; the frontend `src/api/api.js` has an easy fetch wrapper.

Production (serve build from Django):
1. Build the frontend:

```bash
cd frontend
npm run build
```

2. Copy `dist` contents into a Django static directory or configure `STATICFILES_DIRS` to include the `frontend/dist` folder, then run `python manage.py collectstatic`.

3. Create a catch-all view to serve `index.html` for the SPA routes (or configure the web server to do this). Example view:

```py
from django.views.generic import TemplateView

class FrontendAppView(TemplateView):
    template_name = 'index.html'
```

Add route `path('', FrontendAppView.as_view(), name='home')` and ensure `index.html` is in templates/static served area.

Notes:
- For map tiles and real-time vehicle positions, use a small WebSocket/Channels setup or polling endpoints. Django Channels can be added for socket support.
- Keep the React app mobile-first for commuter flows and use the admin routes for larger-screen analytics.
