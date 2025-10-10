# FastAPI + Next.js TODO App

A full-stack TODO application with user authentication, task management, and label organization. Built with FastAPI backend and Next.js frontend, featuring MongoDB for data persistence.

## 🚀 Tech Stack

**Backend:**
- FastAPI 0.104.1 - Modern Python web framework
- MongoDB - NoSQL database with PyMongo driver
- JWT Authentication - Secure token-based auth
- Pydantic - Data validation and serialization
- bcrypt - Password hashing

**Frontend:**
- Next.js 15.5.4 - React framework with App Router
- TypeScript - Type-safe development
- Tailwind CSS - Utility-first styling
- SWR - Data fetching and caching

## 📋 Features

### ✅ Core Features
- **User Management**: Signup, login, logout with JWT tokens
- **Task Management**: Create, read, update, delete tasks
- **Task Status**: Toggle between pending/completed
- **Label System**: Create, assign, and filter tasks by labels
- **Priority Levels**: Low, medium, high priority tasks
- **Due Dates**: Set and track task deadlines
- **Real-time Updates**: Live data synchronization

### 🎯 Stretch Goals
- **Task Filtering**: Filter by labels, status, priority
- **Responsive Design**: Mobile-friendly interface
- **Data Persistence**: All data saved to MongoDB
- **API Documentation**: Interactive Swagger UI at `/docs`

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- MongoDB (local or cloud)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create `.env` file in `backend/` directory:
   ```env
   MONGODB_URL=mongodb://localhost:27017/todoapp
   JWT_SECRET=your-super-secret-jwt-key-here
   ```

4. **Start MongoDB:**
   ```bash
   # Local MongoDB
   mongod
   
   # Or use MongoDB Atlas (cloud)
   # Update MONGODB_URL in .env with your Atlas connection string
   ```

5. **Run the backend:**
   ```bash
   python3 run.py
   ```

Backend will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```

Frontend will be available at `http://localhost:3000`

## 🔧 Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017/todoapp
JWT_SECRET=your-super-secret-jwt-key-here
```

### Frontend
No environment variables needed - uses localhost:8000 for API calls.

## 🚀 Running Locally

### Start Both Services

**Terminal 1 - Backend:**
```bash
cd backend
python3 run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📝 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Tasks
- `GET /api/v1/tasks` - Get user's tasks
- `POST /api/v1/tasks` - Create new task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/status` - Update task status

### Labels
- `GET /api/v1/labels` - Get user's labels
- `POST /api/v1/labels` - Create new label
- `PUT /api/v1/labels/{id}` - Update label
- `DELETE /api/v1/labels/{id}` - Delete label

## 🧪 Testing

Run backend tests:
```bash
cd backend
python -m pytest tests/ -v
```

## 📱 Demo Video

[Demo Video Link - Coming Soon]

## 🏗️ Project Structure

```
fastapi-nextjs-todo/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   ├── core/               # Core utilities
│   ├── crud/               # Database operations
│   ├── models/             # Data models
│   ├── schemas/            # Pydantic schemas
│   ├── tests/              # Test files
│   └── main.py             # FastAPI app
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   └── lib/            # Utility functions
│   └── package.json
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.