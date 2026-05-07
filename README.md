# Task AI Backend

A comprehensive Python backend API for the Task AI project management system, built with FastAPI and SQLAlchemy.

## Features

- **RESTful API** with full CRUD operations
- **JWT Authentication** with secure password hashing
- **PostgreSQL Database** with SQLAlchemy ORM
- **Pydantic Schemas** for data validation
- **Modular Architecture** with separation of concerns
- **CORS Support** for frontend integration
- **Analytics Endpoints** for dashboard metrics

## Project Structure

```
stitch_flow_pro_workspace/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application and routes
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── auth.py              # Authentication utilities
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Database Schema

The backend supports the following main entities:

- **Users**: Authentication and role management
- **Projects**: Project tracking with status and progress
- **Tasks**: Task management with priorities and assignments
- **Team**: Team member information and metrics
- **Analytics**: System metrics and performance data

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Dashboard
- `GET /dashboard/stats` - Dashboard statistics

### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create new project
- `GET /projects/{id}` - Get specific project

### Tasks
- `GET /tasks` - List tasks (with filtering)
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task

### Team
- `GET /team` - List team members
- `POST /team` - Add team member

### Analytics
- `GET /analytics` - General analytics
- `GET /analytics/workload` - Workload intensity data
- `GET /analytics/velocity` - Task velocity metrics
- `GET /analytics/team-distribution` - Team skill distribution

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

Install PostgreSQL and create a database:

```sql
CREATE DATABASE stitchflow_db;
```

### 3. Environment Configuration

Copy the environment template and configure:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials and secret key.

### 4. Run the Application

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

### 5. API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Development

### Database Migrations

For production use, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Testing

Run tests with pytest:

```bash
pytest
```

## Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive data
- Implement rate limiting for production
- Consider using HTTPS in production
- Validate and sanitize all input data

## Frontend Integration

The backend is designed to work seamlessly with the existing frontend files:

- **Analytics Command Center**: Uses `/analytics/*` endpoints
- **Executive Dashboard**: Uses `/dashboard/stats` and `/projects` endpoints
- **Project Board**: Uses `/projects` and `/tasks` endpoints
- **Team Management**: Uses `/team` endpoints

## Example API Usage

```python
import requests

# Login
response = requests.post("http://localhost:8000/auth/login", json={
    "username": "admin",
    "password": "password"
})
token = response.json()["access_token"]

# Get dashboard stats
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/dashboard/stats", headers=headers)
print(response.json())
```

## License

This project is part of the Task AI system.
