# Repo Health Intelligence

AI-powered Git repository analytics platform. Analyzes repositories for engineering risks, code health, hotspots, bus factor, complexity, and architectural decay — with AI-generated insights.

## Stack
- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind, shadcn/ui, Framer Motion, Recharts, React Query
- **Backend**: FastAPI (async), Python 3.11, SQLAlchemy, PostgreSQL
- **Analysis**: GitPython, Tree-sitter, Radon, NetworkX
- **AI**: OpenAI API
- **Deploy**: Docker, Docker Compose, Vercel, Railway/Render

## Quick Start (one command)
```bash
python demo.py
```
This boots Postgres + backend + frontend via Docker Compose and opens the browser.

## Manual Start
```bash
cp .env.example .env       # add your OPENAI_API_KEY
docker compose up --build
```
- Frontend: http://localhost:3000
- Backend:  http://localhost:8000/docs

## Local Dev (no Docker)
Backend:
```bash
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Frontend:
```bash
cd frontend && npm install && npm run dev
```

## Deployment
- **Frontend → Vercel**: import `frontend/` directory, set `NEXT_PUBLIC_API_URL` to your backend URL.
- **Backend → Railway/Render**: deploy from `backend/` directory with `Dockerfile.backend`. Set `DATABASE_URL` and `OPENAI_API_KEY`.

## Features
- Analyze any public GitHub repo (URL + branch)
- Commit history, churn, ownership, bus factor
- Cyclomatic complexity (Radon) + hotspots (complexity × churn)
- Dependency graph (NetworkX) + circular-dependency detection
- Weighted Health Score (0–100) with trend
- AI executive summary, risk insights, recommendations
- Modern animated SaaS dashboard with dark mode
- JWT auth (signup/login)

## API
- `POST /analyze` — kick off repo analysis
- `GET /repositories` — list analyzed repos
- `GET /metrics/{id}`, `/health/{id}`, `/hotspots/{id}`, `/contributors/{id}`, `/graph/{id}`
- `POST /auth/signup`, `POST /auth/login`

