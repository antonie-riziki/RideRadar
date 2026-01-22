# UX Architecture (Commuter + Admin)

Overview
- Mobile-first Commuter experience: single-purpose flows with low cognitive load.
- Web-first Admin dashboard: cards, maps, charts, and AI recommendations.

Commuter screens (priority):
- Home: greeting, quick actions, live status banner.
- Live Map: map with moving vehicles, tap for vehicle sheet.
- Trip / Waiting: countdown, progress, notify toggles, arrive-later suggestions.
- Tickets: QR, offline view, history.
- Notifications center.

Admin screens (priority):
- Overview: KPI cards (active vehicles, commuters, revenue).
- Live Fleet: map + telemetry.
- Analytics: charts, heatmaps, route profitability.
- Management: vehicles, routes, fares, schedules.
- AI Panel: recommendations with confidence & explanation.

Design tokens
- Colors: calming blues/greens (#0b6e99 primary), warm accent (#ff9f43).
- Typography: large sizes for mobile; clear hierarchy for admin.

Integration points
- API: `/api/vehicles`, `/api/routes`, `/api/tickets`, `/api/analytics`, `/ws/` (optional WebSocket for live updates).
- Auth: token/JWT for admin; lightweight session or token for commuter.

Accessibility
- High contrast mode, large tap targets, color-blind safe palettes.

Performance
- Map clustering, tile optimizations, minimal polling intervals (5–15s) or WebSockets.

Internationalization
- English primary, optional Swahili content strings; keep copy short and friendly.
