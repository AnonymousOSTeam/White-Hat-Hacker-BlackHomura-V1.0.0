# BlackHomura - FastAPI scaffold

This repository contains a starter scaffold for the BlackHomura API (BlueTeam) using FastAPI + PostgreSQL.

Roles: admin, analyst, viewer

Quickstart (development):

1. Copy .env.example to .env and fill values (DATABASE_URL, SECRET_KEY)
2. Start services: docker-compose up --build
3. Create DB and seed admin: python scripts/seed_admin.py
4. Run app locally: uvicorn app.main:app --reload --port 8000

Security notes:
- Do NOT store secrets in the repo. Use GitHub Secrets for CI and environment variables in production.
- The seeded admin user has a temporary password; rotate on first login.

Files included: app/, scripts/, alembic/ skeleton, Dockerfile, docker-compose.yml, requirements.txt, .env.example, tests/, .github workflows (CI + CodeQL), dependabot.
