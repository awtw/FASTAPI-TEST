# FastAPI Backend Template

A production-ready FastAPI backend template with Docker, MySQL, Redis, MinIO (S3-compatible storage), and authentication built-in. This template provides a solid foundation for building scalable web applications with modern Python technologies.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Services](#services)
- [Sentry Integration](#sentry-integration)
- [Authentication & Authorization](#authentication--authorization)
- [Database Management](#database-management)
- [API Documentation](#api-documentation)
- [Development Guide](#development-guide)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Docker & Docker Compose** - Containerized development and deployment
- **MySQL 8.3** - Relational database with Adminer GUI
- **Redis 7.0** - In-memory data store for caching and sessions
- **MinIO** - S3-compatible object storage for file uploads
- **Sentry Integration** - Error tracking, performance monitoring, and logging
- **Alembic** - Database migration tool
- **JWT Authentication** - OAuth2 with Bearer tokens
- **Multi-level Authorization** - User, Admin, and Super Admin roles
- **Auto-generated API Documentation** - Swagger UI, ReDoc, and Stoplight Elements
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **Environment-based Configuration** - Easy configuration management
- **Hot Reload** - Development server with automatic code reloading

## Architecture Overview

The template uses a microservices architecture with the following components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   FastAPI App   │─── ▶│     MySQL       │     │     Redis       │
│   (Port 8000)   │     │   (Port 3306)   │     │   (Port 6379)   │
│                 │     │                 │     │                 │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │              ┌─────────────────┐     ┌─────────────────┐
         │              │                 │     │                 │
         └─────────────▶│     MinIO       │     │    Adminer      │
                        │  (Ports 9000/1) │     │   (Port 8001)   │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- Python 3.11+ (for local development)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FastAPI-template
   ```

2. **Set up environment variables**
   ```bash
   cp example.env .env
   # Edit .env file with your configurations if needed
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   - Visit http://localhost:8000/db/renewDB to create database tables
   - This endpoint requires Super Admin authentication (X-SUPER-ADMIN-TOKEN: admin.root)

5. **Access the services**
   - FastAPI Application: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database Admin (Adminer): http://localhost:8001
   - MinIO Console: http://localhost:9001 (admin/admin1234)

## Project Structure

```
FastAPI-template/
├── alembic/                  # Database migration files
│   ├── versions/            # Migration version files
│   ├── env.py              # Alembic environment config
│   └── script.py.mako      # Migration template
├── src/                     # Application source code
│   ├── crud/               # Database CRUD operations
│   │   └── user.py         # User-related CRUD operations
│   ├── database/           # Database configuration
│   │   ├── database.py     # Database connection setup
│   │   ├── models.py       # SQLAlchemy models
│   │   └── utils.py        # Database utilities
│   ├── dependencies/       # FastAPI dependencies
│   │   ├── auth.py         # Authentication dependencies
│   │   └── basic.py        # Basic dependencies
│   ├── routers/           # API route handlers
│   │   ├── db/            # Database management routes
│   │   ├── private/       # Authenticated user routes
│   │   ├── public/        # Public routes
│   │   └── root/          # Admin routes
│   ├── schemas/           # Pydantic models
│   │   ├── base.py        # Base schema classes
│   │   └── basic.py       # Basic schema models
│   ├── utils/             # Utility functions
│   │   ├── credentials.py  # Password & JWT handling
│   │   ├── handler.py      # Error handlers
│   │   ├── s3.py          # S3/MinIO integration
│   │   └── swagger.py      # Custom Swagger UI
│   └── server.py          # Main FastAPI application
├── volume/                # Docker volumes (gitignored)
├── docker-compose.yaml    # Docker services configuration
├── Dockerfile            # Backend container definition
├── requirements.txt      # Python dependencies
├── alembic.ini          # Alembic configuration
├── example.env          # Environment variables template
├── init-minio.sh        # MinIO initialization script
└── minio-entrypoint.sh  # MinIO startup script
```

## Configuration

### Environment Variables

Copy `example.env` to `.env` and configure:

```env
# Database Configuration
DB_HOST=mysql              # MySQL container hostname
DB_USER=admin              # Database user
DB_PASS=admin1234          # Database password
DB_PORT=3306              # MySQL port
DB_NAME=template_db        # Database name

# AWS S3 Configuration (for production)
AWS_ACCESS_KEY_ID=         # AWS access key
AWS_SECRET_ACCESS_KEY=     # AWS secret key
AWS_REGION=                # AWS region
AWS_S3_BUCKET=template-bucket
AWS_CLOUDFRONT_DOMAIN=     # CloudFront distribution domain

# MinIO Configuration (for development)
S3_ENDPOINT_URL=http://minio:9000
S3_PROVIDER=minio          # Use 'aws' for production
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin1234
MINIO_DNS_URL=http://localhost:9000

# API Keys
ADMIN_API_KEY=admin        # Admin API key
SUPER_ADMIN_API_KEY=admin.root  # Super Admin API key

# Sentry Configuration (Optional - Get DSN from sentry.io)
SENTRY_DSN=                # Your Sentry DSN
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_PROFILES_SAMPLE_RATE=1.0
```

## Services

### Backend (FastAPI)

The main application service running on port 8000:

- **Framework**: FastAPI with Uvicorn ASGI server
- **Features**: Auto-reload, CORS enabled, JWT authentication
- **Endpoints**: Public, Private (authenticated), Admin, and Database management

### MySQL Database

Relational database for persistent data storage:

- **Version**: MySQL 8.3
- **Default Database**: template_db
- **Root Password**: root
- **User Credentials**: admin/admin1234
- **Data Persistence**: ./volume/mysql_data

### Redis Cache

In-memory data store for caching and sessions:

- **Version**: Redis 7.0 Alpine
- **Port**: 6379 (internal only)
- **Data Persistence**: ./volume/redis_data

### MinIO Object Storage

S3-compatible object storage for file uploads:

- **API Port**: 9000
- **Console Port**: 9001
- **Default Bucket**: template-bucket (public read access)
- **Credentials**: admin/admin1234
- **Data Persistence**: ./volume/minio_data

### Adminer

Web-based database management tool:

- **Port**: 8001
- **Supported Databases**: MySQL, PostgreSQL, SQLite, MS SQL
- **Login with**: Server: mysql, Username: admin, Password: admin1234

## Sentry Integration

The template includes comprehensive Sentry integration for error tracking, performance monitoring, and logging. Sentry is **optional** and disabled by default.

### Features

- **Error Tracking** - Automatic capture of unhandled exceptions
- **Performance Monitoring** - Track API endpoint, database, and Redis performance
- **Logging Integration** - All ERROR+ logs sent to Sentry as events
- **Request Context** - Full request details with every error
- **Distributed Tracing** - Track requests across your microservices

### Integrations Included

1. **FastAPI Integration** - Request/response tracking and error capture
2. **SQLAlchemy Integration** - Database query monitoring
3. **Redis Integration** - Redis operation tracking
4. **Logging Integration** - Automatic log capture
5. **Threading Integration** - Background thread error tracking

### Quick Setup

1. **Create a Sentry account** at [sentry.io](https://sentry.io) (free tier available)
2. **Create a FastAPI project** and copy your DSN
3. **Add to your `.env` file:**
   ```env
   SENTRY_DSN=https://your-sentry-dsn@sentry.io/your-project-id
   ```
4. **Restart the application:**
   ```bash
   docker-compose restart backend
   ```

### Testing Sentry

Test endpoints are available at:
- `/test-sentry-error` - Triggers a test error
- `/test-sentry-logging` - Tests logging integration
- `/test-sentry-capture` - Tests manual message capture

### Configuration

The application monitors:
- All API endpoint performance
- Database query execution times
- Redis operation latency
- Application logs (ERROR+ as events, INFO+ as breadcrumbs)

For production best practices, advanced configuration, and detailed documentation, see **[SENTRY.md](SENTRY.md)**.

## Authentication & Authorization

### Authentication Flow

1. **Login**: POST to `/public/auth/login` with username/password
2. **Token**: Receive JWT token in response
3. **Authorization**: Include token in Authorization header: `Bearer <token>`

### Authorization Levels

1. **Public Routes** (`/public/*`)
   - No authentication required
   - Login endpoint available here

2. **Private Routes** (`/private/*`)
   - Requires valid JWT token
   - For authenticated users

3. **Admin Routes** (`/root/*`)
   - Requires X-ADMIN-TOKEN header
   - Default: `admin`

4. **Super Admin Routes** (`/db/*`)
   - Requires X-SUPER-ADMIN-TOKEN header
   - Default: `admin.root`
   - Database management operations

### Test Credentials

Default test user (created via /db/renewDB):
```
Username: test-username
Password: test-password
```

## Database Management

### Models

The template includes three main models:

1. **User** - Basic user information
   - id (UUID)
   - name (unique, 16 chars)
   - created_at, updated_at timestamps

2. **UserAccount** - Authentication credentials
   - username (unique, 16 chars)
   - password (hashed)
   - Linked to User model

3. **Blob** - File metadata storage
   - content_type
   - filename
   - url (S3/MinIO URL)
   - Many-to-many relationship with Users

### Database Operations

**Initialize/Reset Database:**
```bash
curl -X POST http://localhost:8000/db/renew \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"
```

**Run Alembic Migrations (API):**
```bash
# Full migration (delete old versions, create revision, and upgrade)
curl -X POST http://localhost:8000/db/alembic \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"

# Skip revision generation (only upgrade existing migrations)
curl -X POST "http://localhost:8000/db/alembic?skip_revision=true" \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"

# Keep existing version files
curl -X POST "http://localhost:8000/db/alembic?delete_first=false" \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"
```

### Migrations with Alembic (Manual)

**Create a new migration:**
```bash
docker exec template-backend alembic revision --autogenerate -m "Description"
```

**Apply migrations:**
```bash
docker exec template-backend alembic upgrade head
```

**Rollback migration:**
```bash
docker exec template-backend alembic downgrade -1
```

## API Documentation

The template provides three different API documentation interfaces:

1. **Swagger UI** (Interactive)
   - URL: http://localhost:8000/docs
   - Features: Try out endpoints, authentication support
   - Custom dark theme included

2. **ReDoc** (Clean Documentation)
   - URL: http://localhost:8000/redoc
   - Features: Clean, readable API documentation

3. **Stoplight Elements** (Modern UI)
   - URL: http://localhost:8000/elements
   - Features: Modern design, code samples

## Development Guide

### Local Development Setup

1. **Install Python dependencies locally:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **IDE Configuration:**
   - Set Python interpreter to venv
   - Configure PYTHONPATH to include project root
   - Enable type checking for better code completion

3. **Hot Reload:**
   - The Docker container runs with `--reload` flag
   - Changes to Python files automatically restart the server

### Adding New Features

**1. Create a new model:**
```python
# src/database/models.py
class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    # Add more fields
```

**2. Create CRUD operations:**
```python
# src/crud/new_model.py
from sqlalchemy.orm import Session
from src.database import models

def create_item(db: Session, name: str):
    item = models.NewModel(id=str(ulid.new()), name=name)
    db.add(item)
    db.commit()
    return item
```

**3. Create schemas:**
```python
# src/schemas/new_model.py
from pydantic import BaseModel

class NewModelCreate(BaseModel):
    name: str

class NewModelResponse(BaseModel):
    id: str
    name: str
    
    class Config:
        from_attributes = True
```

**4. Create router:**
```python
# src/routers/private/new_model.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies.basic import get_db
from src.crud import new_model as crud
from src.schemas import new_model as schemas

router = APIRouter()

@router.post("/", response_model=schemas.NewModelResponse)
def create_item(
    item: schemas.NewModelCreate,
    db: Session = Depends(get_db)
):
    return crud.create_item(db, item.name)
```

### Working with S3/MinIO

**Upload a file:**
```python
from src.utils.s3 import s3_client
import ulid

# Upload file
file_key = f"uploads/{ulid.new()}/filename.jpg"
s3_client.upload_file("local_file.jpg", "template-bucket", file_key)

# Get public URL
url = f"http://localhost:9000/template-bucket/{file_key}"
```


## Production Deployment

### Environment Configuration

1. **Update .env for production:**
   ```env
   S3_PROVIDER=aws
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_REGION=us-east-1
   ADMIN_API_KEY=strong-random-key
   SUPER_ADMIN_API_KEY=very-strong-random-key
   
   # Sentry for production monitoring
   SENTRY_DSN=your-production-dsn
   SENTRY_ENVIRONMENT=production
   SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% sampling to reduce costs
   SENTRY_PROFILES_SAMPLE_RATE=0.1
   ```

2. **Update docker-compose.yaml:**
   - Remove development volumes
   - Change command to use `gunicorn` instead of `--reload`
   - Add health checks

3. **Security considerations:**
   - Use strong, unique passwords
   - Enable HTTPS with SSL certificates
   - Implement rate limiting
   - Add request validation
   - Use environment-specific configurations
   - Configure Sentry to filter sensitive data (see [SENTRY.md](SENTRY.md))
   - Reduce Sentry sampling rates in production to control costs

### Deployment Options

**1. Docker Swarm:**
```bash
docker stack deploy -c docker-compose.yaml app-stack
```

**2. Kubernetes:**
- Convert docker-compose to K8s manifests
- Use ConfigMaps for environment variables
- Set up Ingress for load balancing

**3. Cloud Platforms:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

### Database Backups

**Manual backup:**
```bash
docker exec template-mysql mysqldump -u admin -padmin1234 template_db > backup.sql
```

**Restore backup:**
```bash
docker exec -i template-mysql mysql -u admin -padmin1234 template_db < backup.sql
```

## Troubleshooting

### Common Issues

**1. Container fails to start:**
- Check logs: `docker-compose logs backend`
- Ensure all ports are available
- Verify environment variables

**2. Database connection errors:**
- Wait for MySQL to fully initialize
- Check credentials in .env
- Ensure mysql container is running

**3. MinIO bucket not accessible:**
- Check if initialization script ran
- Verify MinIO credentials
- Ensure bucket policy is applied

**4. Authentication failures:**
- Verify JWT token is included in headers
- Check token expiration
- Ensure API keys match .env values

### Debug Commands

```bash
# View all logs
docker-compose logs -f

# Check container status
docker-compose ps

# Enter container shell
docker exec -it template-backend bash

# Test database connection
docker exec template-mysql mysql -u admin -padmin1234 -e "SHOW DATABASES;"

# Check Redis connection
docker exec template-redis redis-cli ping
```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down

# Remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Clean rebuild
docker-compose build --no-cache
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.