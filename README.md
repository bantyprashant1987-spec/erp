# Retail Billing ERP (Offline-first ready)

FastAPI + PostgreSQL + React (Vite) full-stack billing/inventory starter with JWT auth, multi-shop support (shop_id on all business tables), and Docker-based deployment.

## Features (MVP)
- Owner/Staff authentication with JWT
- Multi-shop data isolation
- Product CRUD with stock and low-stock threshold
- Billing screen: cart, discount, GST, payment modes, auto stock deduction
- Sales reporting: daily summary
- Clean architecture: routers, schemas, services, models separated
- Dockerized (backend, frontend via nginx, postgres)

## Project Structure
- backend/app: FastAPI app (routers, services, models, schemas)
- frontend: React Vite SPA with simple dashboard/billing UI
- docker-compose.yml: postgres + backend + frontend
- .env.example: configuration template

## Quick Start (Docker)
1. Copy env template: `cp .env.example .env` (update secrets/passwords).
2. Build & run: `docker compose up --build`.
3. Backend API: http://localhost:8000/api
4. Frontend: http://localhost:8080
5. Default owner login: `owner@example.com` / `changeme123`

## Local Dev (backend)
- Create virtualenv, install deps: `pip install -r backend/requirements.txt`
- Set `DATABASE_URL` to your Postgres instance.
- Run: `uvicorn app.main:app --reload --app-dir backend`

## Local Dev (frontend)
- `cd frontend && npm install`
- `npm run dev` (default at http://localhost:5173)
- Set `VITE_API_URL` in `.env` for frontend to point to backend (e.g. http://localhost:8000/api).

## Notes
- UUID primary keys; `shop_id` present on Product/Sale/SaleItem/User for isolation.
- Tables auto-created on startup; default owner seeded from `ADMIN_EMAIL`/`ADMIN_PASSWORD`.
- Nginx proxies `/api` to backend container.
- For production, set strong `SECRET_KEY`, tighten CORS, and place services on private network.

## Deploy to Render
1) Push main to GitHub, then in Render choose **New > Blueprint** and point to this repo; Render will read [render.yaml](render.yaml) to create backend, frontend, and Postgres.
2) After provisioning, edit environment variables: set a long `SECRET_KEY`, change `ADMIN_PASSWORD`, set `CORS_ORIGINS` to your frontend Render URL, and set the frontend `VITE_API_URL` to your backend URL with `/api` suffix.
3) Blueprint creates a managed Postgres (`erp-db`); `DATABASE_URL` is injected automatically. No `.env` files are needed on Render.
4) First login uses the owner credentials you set in env vars. Health check: `/health` on backend.
