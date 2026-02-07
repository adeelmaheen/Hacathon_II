# Todo Web App - Backend API

High-performance RESTful API for task management built with FastAPI, SQLModel, and PostgreSQL.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.14+ (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL 15+ (Neon cloud-hosted)
- **Authentication**: JWT (python-jose) + bcrypt
- **Migrations**: Alembic
- **Python**: 3.11+
- **Validation**: Pydantic 2.5+

## Features

- ✅ RESTful API with OpenAPI (Swagger) documentation
- ✅ JWT-based authentication with HTTPOnly cookies
- ✅ User data isolation (user-scoped queries)
- ✅ CRUD operations for tasks
- ✅ Password hashing with bcrypt
- ✅ Database migrations with Alembic
- ✅ Type-safe ORM with SQLModel
- ✅ Automatic request/response validation
- ✅ CORS configuration for frontend integration

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+ (local or cloud-hosted)
- pip or poetry for dependency management

## Getting Started

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Update the environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | Random 32+ character string |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` (default) |
| `JWT_EXPIRATION_HOURS` | Token validity period | `24` (default) |

### 3. Database Setup

#### Option A: Local PostgreSQL

```bash
# Create database
createdb todo_db

# Or using psql
psql -U postgres
CREATE DATABASE todo_db;
\q
```

#### Option B: Neon (Cloud PostgreSQL)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `.env`

#### Run Migrations

```bash
# Initialize Alembic (already done in project)
# alembic init alembic

# Create migration for schema changes
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 4. Run Development Server

```bash
# Start server with auto-reload
uvicorn src.main:app --reload --port 8000

# Or with custom host
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Run with Docker Compose

```bash
# From project root
docker-compose up backend

# With rebuild
docker-compose up --build backend
```

## Project Structure

```
backend/
├── src/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment config
│   ├── db.py                    # Database connection
│   ├── models/                  # SQLModel database models
│   │   ├── user.py              # User model
│   │   └── task.py              # Task model
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── auth.py              # Auth schemas
│   │   └── task.py              # Task schemas
│   ├── services/                # Business logic
│   │   ├── auth_service.py      # Authentication logic
│   │   └── task_service.py      # Task CRUD logic
│   ├── api/                     # API route handlers
│   │   ├── deps.py              # Dependency injection
│   │   ├── auth.py              # Auth endpoints
│   │   └── tasks.py             # Task endpoints
│   └── utils/                   # Utilities
│       └── security.py          # Password hashing, JWT
├── alembic/                     # Database migrations
│   ├── versions/                # Migration files
│   └── env.py                   # Alembic config
├── tests/                       # Test files (optional)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── alembic.ini                  # Alembic configuration
├── Dockerfile                   # Docker config
└── README.md                    # This file
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| POST | `/api/auth/logout` | Logout user | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks` | Get all user tasks | Yes |
| POST | `/api/tasks` | Create new task | Yes |
| PUT | `/api/tasks/{id}` | Update task | Yes |
| PATCH | `/api/tasks/{id}/toggle` | Toggle completion | Yes |
| DELETE | `/api/tasks/{id}` | Delete task | Yes |

## API Documentation

### Register User

**POST** `/api/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-03T12:00:00Z"
}
```

### Login

**POST** `/api/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Note**: JWT token is also set as HTTPOnly cookie.

### Create Task

**POST** `/api/tasks`

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Write README files for frontend and backend"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": "uuid-here",
  "title": "Complete project documentation",
  "description": "Write README files for frontend and backend",
  "completed": false,
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:00:00Z"
}
```

### Get All Tasks

**GET** `/api/tasks`

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": "uuid-here",
    "title": "Complete project documentation",
    "description": "Write README files",
    "completed": false,
    "created_at": "2026-01-03T12:00:00Z",
    "updated_at": "2026-01-03T12:00:00Z"
  }
]
```

### Update Task

**PUT** `/api/tasks/{id}`

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "uuid-here",
  "title": "Updated title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:05:00Z"
}
```

### Toggle Task Completion

**PATCH** `/api/tasks/{id}/toggle`

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "completed": true,
  "updated_at": "2026-01-03T12:10:00Z"
}
```

### Delete Task

**DELETE** `/api/tasks/{id}`

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:** `204 No Content`

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## Authentication Flow

1. **Registration**:
   - User submits email, name, password
   - Password hashed with bcrypt
   - User record created in database
   - User details returned (password excluded)

2. **Login**:
   - User submits email, password
   - Password verified against hash
   - JWT token generated with user_id in `sub` claim
   - Token set as HTTPOnly cookie + returned in response

3. **Protected Routes**:
   - Extract JWT from Authorization header or cookie
   - Decode and verify token
   - Extract user_id from `sub` claim
   - Use user_id to scope database queries

## Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Signed with secret key
- **HTTPOnly Cookies**: Prevent XSS attacks
- **User Data Isolation**: All queries filtered by user_id
- **CORS**: Configured for frontend origin
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection Prevention**: SQLModel ORM (no raw SQL)

## Available Scripts

| Command | Description |
|---------|-------------|
| `uvicorn src.main:app --reload` | Start dev server |
| `alembic upgrade head` | Run migrations |
| `alembic revision --autogenerate -m "msg"` | Create migration |
| `pytest` | Run tests (when added) |
| `black src/` | Format code |
| `mypy src/` | Type checking |

## Database Migrations

### Create New Migration

```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Add new field to tasks"

# Apply migration
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

### View Migration History

```bash
alembic history
alembic current
```

## Deployment

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t todo-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  -e JWT_SECRET_KEY="your-secret" \
  todo-backend
```

### Docker Compose

```bash
# Start all services (backend + database)
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Cloud Platforms

#### Render

1. Push code to GitHub
2. Create new Web Service in Render
3. Connect GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy

#### Railway

```bash
railway login
railway init
railway add
railway up
```

#### AWS/GCP/Azure

Deploy using:
- **AWS Elastic Beanstalk**: Python platform
- **Google Cloud Run**: Container deployment
- **Azure App Service**: Python runtime

**Build command**: `pip install -r requirements.txt`
**Start command**: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

## Environment-Specific Configs

### Development

```env
DATABASE_URL=postgresql://localhost:5432/todo_dev
JWT_SECRET_KEY=dev-secret-key-not-for-production
JWT_EXPIRATION_HOURS=24
```

### Production

```env
DATABASE_URL=postgresql://prod-host:5432/todo_prod
JWT_SECRET_KEY=<generate-secure-random-key>
JWT_EXPIRATION_HOURS=24
```

**Generate secure JWT secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Testing

### Manual Testing with cURL

**Register**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User","password":"password123"}'
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt
```

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Test task","description":"Test description"}'
```

### Interactive API Docs

Visit **http://localhost:8000/docs** for Swagger UI where you can:
- Test all endpoints
- See request/response schemas
- Authorize with JWT token

## Troubleshooting

### Database Connection Issues

**Problem**: `FATAL: database "todo_db" does not exist`

**Solution**:
```bash
createdb todo_db
# Or in psql:
CREATE DATABASE todo_db;
```

**Problem**: `FATAL: role "user" does not exist`

**Solution**:
```bash
createuser -s user
# Or in psql:
CREATE USER user WITH PASSWORD 'password';
```

### Migration Issues

**Problem**: `alembic.util.exc.CommandError: Target database is not up to date`

**Solution**:
```bash
alembic upgrade head
```

**Problem**: Migration conflicts

**Solution**:
```bash
# Check current version
alembic current

# View history
alembic history

# Stamp to specific version
alembic stamp head
```

### JWT Token Issues

**Problem**: `401 Unauthorized - Invalid token`

**Solution**:
- Check JWT_SECRET_KEY matches between token creation and validation
- Ensure token hasn't expired
- Verify Authorization header format: `Bearer <token>`

### CORS Issues

**Problem**: Frontend cannot connect to backend

**Solution**:
Update CORS origins in `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance

- **Response time**: <200ms p95 for CRUD operations
- **Concurrent users**: 100+ without degradation
- **Database pooling**: SQLAlchemy connection pool
- **Async support**: FastAPI's native async/await

## Monitoring

### Health Check

```bash
curl http://localhost:8000/
```

### Database Connection

Check active connections:
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'todo_db';
```

## Contributing

1. Follow PEP 8 style guide
2. Use type hints for all functions
3. Run Black formatter before committing
4. Use Pydantic models for validation
5. Write docstrings for all public functions
6. Keep business logic in services, not routes

## Code Quality

```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/

# Security scanning
bandit -r src/
```

## License

MIT

## Support

For issues or questions:
- Check the [specification](../specs/001-todo-web-app/spec.md)
- Review the [implementation plan](../specs/001-todo-web-app/plan.md)
- See [frontend README](../frontend/README.md) for client integration
- Visit interactive docs at http://localhost:8000/docs
