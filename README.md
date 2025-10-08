# FastAPI TODO App

A simple TODO application with FastAPI backend and MongoDB database.

## Features
- User registration and login
- Create, read, update, and delete todos
- User-specific todo management

## Quick Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   python setup.py
   # Edit .env file with your MongoDB connection
   ```

3. **Start server**:
   ```bash
   python main.py
   ```

4. **Test API**:
   - Server: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Endpoints

### Auth
- `POST /auth/register` - Register user
- `POST /auth/login` - Login user

### Todos
- `POST /todos` - Create todo
- `GET /todos/{user_id}` - Get user todos
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Delete todo

## Example Usage

Register user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "password123"}'
```

Create todo:
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "user_id": "USER_ID_HERE"}'
```