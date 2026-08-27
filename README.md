# BlackHomura - FastAPI Scaffold

A defensive hacking & incident response API scaffold built with **FastAPI** + **PostgreSQL**.

## Features

- **Role-Based Access Control**: admin, analyst, viewer
- **JWT Authentication**: OAuth2 with JWT tokens
- **Incident Management**: Track security incidents
- **Asset Management**: Manage network assets
- **IOC Tracking**: Indicators of Compromise database
- **Docker Support**: Containerized development & deployment

## Quick Start

### 1. Clone & Setup Environment

```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL, SECRET_KEY, and PostgreSQL credentials
```

### 2. Start with Docker Compose

```bash
docker-compose up --build
```

This starts:
- PostgreSQL 15 on localhost:5432
- FastAPI on localhost:8000

### 3. Initialize Database

In another terminal:

```bash
docker-compose exec web python scripts/seed_admin.py
```

Default admin credentials:
- **Username**: `admin`
- **Password**: `ChangeMe123!`
- ⚠️ Change this password on first login!

### 4. Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Running Locally (Without Docker)

### Prerequisites

- Python 3.11+
- PostgreSQL 15+

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/blackhomura"
export SECRET_KEY="your-secret-key"

# Create tables
python -c "from app.db import create_db_and_tables; create_db_and_tables()"

# Seed admin user
python scripts/seed_admin.py

# Run the server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/
```

## API Endpoints

### Authentication
| POST | `/auth/token` | Login and get JWT token |

### Users (Admin Only)
| POST | `/users` | Create new user |
| GET | `/users` | List all users |
| GET | `/users/me` | Get current user info |

### Incidents
| GET | `/incidents` | List incidents |
| POST | `/incidents` | Create incident (analyst+) |
| GET | `/incidents/{id}` | Get incident details |
| PUT | `/incidents/{id}` | Update incident (analyst+) |

### Assets
| GET | `/assets` | List assets |
| POST | `/assets` | Create asset (analyst+) |

### IOCs (Indicators of Compromise)
| GET | `/iocs` | List IOCs |
| POST | `/iocs` | Create IOC (analyst+) |
| GET | `/iocs/{id}` | Get IOC details |

## Roles & Permissions

| Role | Permissions |
|------|-------------|
| **admin** | Create/list users, all analyst permissions |
| **analyst** | Create/update incidents, assets, IOCs |
| **viewer** | Read-only access to incidents, assets, IOCs |

## Example Usage

### Login

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=ChangeMe123!"
```

### Create Incident

```bash
curl -X POST "http://localhost:8000/incidents" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Suspicious Login Attempt",
    "description": "Multiple failed login attempts from 192.168.1.100",
    "status": "open"
  }'
```

## Security Notes

⚠️ **Important**

- **NEVER** commit `.env` with real secrets
- **ALWAYS** change `SECRET_KEY` in production
- Use GitHub Secrets for CI/CD pipelines
- Rotate admin password immediately after first login
- Enable HTTPS in production
- Use strong, unique database passwords

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app & endpoints
│   ├── models.py        # SQLModel ORM models
│   └── db.py            # Database configuration
├── scripts/
│   └── seed_admin.py    # Database initialization
├── tests/
│   └── test_basic.py    # Basic API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Troubleshooting

### Docker won't start

```bash
docker-compose logs web
docker-compose down -v
docker-compose up --build
```

### Database connection errors

- Verify DATABASE_URL in `.env`
- Check PostgreSQL: `docker-compose ps`
- Restart: `docker-compose restart db web`

## License

See LICENSE file for details.
