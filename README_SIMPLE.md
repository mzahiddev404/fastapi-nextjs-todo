# Todo List API

A production-ready RESTful API for managing todo items built with FastAPI and MongoDB, featuring user authentication, advanced security, and comprehensive monitoring.

## Features

✅ **Full CRUD operations** for todo items  
🔍 **Advanced search functionality** with text indexing  
📊 **Filtering by completion status, priority, and labels**  
📄 **Pagination support** with lazy loading  
🏷️ **Priority levels** (low, medium, high)  
📝 **Detailed descriptions** and due dates  
🕐 **Automatic timestamps** with timezone support  
🔄 **Async/await support** throughout  
📚 **Auto-generated API documentation** with Swagger UI  
🔐 **User authentication** with JWT tokens  
🛡️ **Rate limiting** and security headers  
📊 **Health monitoring** and performance metrics  
🧪 **Comprehensive testing** with 80%+ coverage  

## Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (local or remote)
- Node.js 16+ (for frontend)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd fastapi-nextjs-todo
```

2. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
```

3. **Configure your .env file:**
```env
# MongoDB Configuration
project_db_url=mongodb://localhost:27017
project_db_name=todo_app_db

# FastAPI Configuration
API_HOST=127.0.0.1
API_PORT=8000

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

4. **Start MongoDB (if running locally):**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or using system service
sudo systemctl start mongod
```

5. **Run the application:**
```bash
# Simple run (with auto-reload)
python main.py

# Or using the run script
python run_simple.py
```

The API will be available at http://localhost:8000

6. **Frontend Setup (Optional):**
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Register a new user |
| POST | `/api/v1/auth/login` | Login user |
| GET | `/api/v1/auth/me` | Get current user info |

### Todo Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks/` | Create a new task |
| GET | `/api/v1/tasks/` | Get all tasks (with filtering) |
| GET | `/api/v1/tasks/{id}` | Get a specific task |
| PUT | `/api/v1/tasks/{id}` | Update a task |
| DELETE | `/api/v1/tasks/{id}` | Delete a task |
| PATCH | `/api/v1/tasks/{id}/status` | Update task status |
| GET | `/api/v1/tasks/stats` | Get task statistics |

### Label Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/labels/` | Create a new label |
| GET | `/api/v1/labels/` | Get all labels |
| PUT | `/api/v1/labels/{id}` | Update a label |
| DELETE | `/api/v1/labels/{id}` | Delete a label |

### Health & Monitoring
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Basic health check |
| GET | `/api/v1/health` | Detailed health check |
| GET | `/api/v1/health/metrics` | System metrics |

## Usage Examples

### Create a User Account
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "password": "SecurePass123!"
     }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "SecurePass123!"
     }'
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Complete the FastAPI tutorial",
       "priority": "high",
       "due_date": "2024-12-31"
     }'
```

### Get All Tasks
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/tasks/"
```

### Filter Tasks
```bash
# Get only completed tasks
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/tasks/?status=completed"

# Get high priority tasks
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/tasks/?priority=high"

# Pagination
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/tasks/?skip=0&limit=10"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/{task_id}" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "title": "Learn FastAPI Advanced",
       "status": "completed"
     }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/{task_id}" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Data Model

### User
```json
{
  "id": "string",
  "username": "string (required, 3-50 chars)",
  "email": "string (required, valid email)",
  "is_active": "boolean (default: true)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Task Item
```json
{
  "id": "string",
  "title": "string (required, 1-100 chars)",
  "description": "string (optional, max 500 chars)",
  "status": "string (pending|completed, default: pending)",
  "priority": "string (low|medium|high, default: medium)",
  "due_date": "datetime (optional)",
  "labels": "array of label objects",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_id": "string"
}
```

### Label
```json
{
  "id": "string",
  "name": "string (required, 1-50 chars)",
  "color": "string (hex color code)",
  "user_id": "string",
  "created_at": "datetime"
}
```

## Development

### Project Structure
```
fastapi-nextjs-todo/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── run_simple.py        # Simple run script with auto-reload
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── crud/                # CRUD operations
│   ├── api/v1/              # API routes
│   ├── core/                # Core functionality
│   ├── middleware/          # Custom middleware
│   ├── tests/               # Test suite
│   └── requirements.txt     # Python dependencies
├── frontend/                # Next.js frontend
└── docs/                    # Documentation
```

### Running in Development Mode

The application runs with auto-reload enabled by default when started with `python main.py`.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `project_db_url` | MongoDB connection URL | `mongodb://localhost:27017` |
| `project_db_name` | Database name | `todo_app_db` |
| `API_HOST` | API host | `127.0.0.1` |
| `API_PORT` | API port | `8000` |
| `JWT_SECRET` | JWT secret key | Required |
| `ENVIRONMENT` | Environment | `development` |
| `DEBUG` | Debug mode | `true` |

### Error Handling

The API includes comprehensive error handling:

- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error
- **503**: Service Unavailable (database connection issues)

### Database

The application uses MongoDB with the following features:

- **Automatic database and collection creation**
- **Optimized indexes** for better performance
- **Text search capabilities** on task content
- **Async operations** with Motor driver
- **Connection pooling** and timeout management

### Database Indexes

- `created_at`: For sorting by creation date
- `user_id`: For user-specific queries
- `status`: For filtering by completion status
- `priority`: For filtering by priority
- `due_date`: For date-based filtering
- **Text index** on title and description: For search functionality
- **Compound indexes** for complex queries

## Production Features

### Security
- JWT authentication with refresh tokens
- Password strength validation
- Rate limiting (5/min auth, 100/min API)
- CORS protection
- Security headers (XSS, CSRF protection)
- Input validation and sanitization

### Performance
- Redis caching with fallback
- Database query optimization
- Lazy loading and pagination
- Connection pooling
- Performance monitoring

### Monitoring
- Health check endpoints
- System metrics tracking
- Error tracking and reporting
- Request/response time monitoring
- Database performance metrics

### Testing
- Comprehensive test suite (80%+ coverage)
- Unit, integration, and security tests
- Automated testing pipeline
- Performance testing

## License

This project is created for educational purposes.

## About

Production-ready todo app with enterprise-grade features, built with modern web technologies and best practices.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [API Documentation](http://localhost:8000/docs)
