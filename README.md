# FastAPI TODO App

A modern TODO application built with FastAPI and MongoDB using Motor for async operations.

## Features

- **User Authentication**: JWT-based authentication with bcrypt password hashing
- **Task Management**: Create, read, update, and delete tasks
- **Label System**: Organize tasks with custom labels and colors
- **Async Operations**: Full async/await support with Motor
- **RESTful API**: Clean REST API design with proper HTTP status codes
- **Data Validation**: Pydantic models for request/response validation
- **Docker Support**: Ready for containerized deployment

## Project Structure

```
app/
├── core/
│   ├── config.py      # Configuration settings
│   ├── db.py          # Database connection
│   └── security.py    # Authentication utilities
├── models/
│   ├── user.py        # User model
│   ├── task.py        # Task model
│   └── label.py       # Label model
├── schemas/
│   ├── user.py        # User schemas
│   ├── task.py        # Task schemas
│   └── label.py       # Label schemas
├── crud/
│   ├── user.py        # User CRUD operations
│   ├── task.py        # Task CRUD operations
│   └── label.py       # Label CRUD operations
├── api/
│   └── v1/
│       ├── auth.py    # Authentication endpoints
│       ├── tasks.py   # Task endpoints
│       └── labels.py  # Label endpoints
└── main.py            # FastAPI application
```

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository
2. Copy `env.example` to `.env` and configure your settings
3. Run with Docker Compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export MONGODB_URI="mongodb://localhost:27017"
export JWT_SECRET="your-secret-key"
export JWT_ALGO="HS256"
```

3. Start MongoDB (if not using Docker)

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Tasks
- `GET /api/v1/tasks/` - Get all tasks
- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `GET /api/v1/tasks/completed` - Get completed tasks
- `GET /api/v1/tasks/pending` - Get pending tasks

### Labels
- `GET /api/v1/labels/` - Get all labels
- `POST /api/v1/labels/` - Create new label
- `GET /api/v1/labels/{label_id}` - Get specific label
- `PUT /api/v1/labels/{label_id}` - Update label
- `DELETE /api/v1/labels/{label_id}` - Delete label
- `GET /api/v1/labels/{label_id}/tasks` - Get tasks by label

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Environment Variables

- `MONGODB_URI`: MongoDB connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_ALGO`: JWT algorithm (default: HS256)
- `DEBUG`: Enable debug mode (default: false)

## Development

The application follows these principles:
- Small, focused functions with clear responsibilities
- Comprehensive error handling
- Async/await throughout
- Type hints for better code clarity
- Modular architecture with clear separation of concerns