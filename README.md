# My TODO App

A production-ready task management application built with FastAPI and Next.js 15, featuring real-time updates and secure authentication.

## 📚 Documentation

**👉 [User Guide](./PROJECT_DOCUMENTATION.md)**

Complete documentation for users and developers.

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

## ✨ Features

- **Secure Authentication**: JWT-based login and registration
- **Task Management**: Create, edit, and organize your tasks
- **Smart Organization**: Custom labels and status filtering
- **Real-time Updates**: Instant synchronization across devices
- **User Profiles**: Track your productivity and task statistics
- **Mobile Ready**: Responsive design for all devices

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python3 run.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Setup
Create `.env` file in backend directory:
```env
MONGODB_URL=mongodb://localhost:27017/todoapp
JWT_SECRET=your-super-secret-jwt-key-here
```

## 📁 Project Structure

```
├── backend/          # FastAPI API server
├── frontend/         # Next.js web app
└── docs/            # Documentation
```

## 🚀 Deployment

- **Backend**: Deploy to Railway, Heroku, or similar
- **Frontend**: Deploy to Vercel or Netlify
- **Database**: Use MongoDB Atlas for production