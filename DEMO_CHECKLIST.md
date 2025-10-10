# Demo Checklist for AI VibeCoding TODO App

## 🎥 Demo Recording Guide

### 1. Project Overview (30 seconds)
- Show the project structure (backend/ and frontend/ folders)
- Highlight the tech stack: FastAPI + Next.js + MongoDB
- Mention the key features: authentication, task management, labels

### 2. Backend API Demonstration (2 minutes)

#### API Documentation
- Navigate to `http://localhost:8000/docs`
- Show the interactive Swagger UI
- Highlight the three main endpoint groups:
  - **Authentication** (`/api/v1/auth/`)
  - **Tasks** (`/api/v1/tasks/`)
  - **Labels** (`/api/v1/labels/`)

#### Test Key Endpoints
- **POST /api/v1/auth/signup** - Create a new user
- **POST /api/v1/auth/login** - Login and get JWT token
- **GET /api/v1/auth/me** - Get current user info
- **POST /api/v1/tasks** - Create a new task
- **GET /api/v1/tasks** - List user's tasks
- **POST /api/v1/labels** - Create a new label
- **GET /api/v1/labels** - List user's labels

### 3. Frontend Application Demo (3 minutes)

#### User Authentication Flow
1. **Signup Process**
   - Go to `http://localhost:3000`
   - Click "Create a new account"
   - Fill out signup form (username, email, password)
   - Show successful registration and auto-login

2. **Login Process**
   - Logout from the app
   - Click "Sign in to your account"
   - Enter credentials and login
   - Show successful authentication

#### Task Management Features
1. **Create Tasks**
   - Add a new task with title, description, priority
   - Set a due date
   - Assign labels to the task
   - Show task appears in the list

2. **Task Operations**
   - Toggle task status (pending ↔ completed)
   - Edit task details (click Edit button)
   - Delete a task (click Delete button)
   - Show real-time updates

3. **Task Filtering**
   - Create multiple tasks with different labels
   - Use the label filter in the sidebar
   - Show tasks filtered by selected label
   - Clear filter to show all tasks

#### Label Management
1. **Create Labels**
   - Add new labels with different colors
   - Show labels appear in the sidebar
   - Demonstrate color coding

2. **Label Operations**
   - Edit existing labels
   - Delete labels
   - Show task counts for each label

### 4. Technical Highlights (1 minute)

#### Code Quality
- Show the clean project structure
- Highlight TypeScript usage in frontend
- Show Python type hints in backend
- Demonstrate modular architecture

#### Database Integration
- Show MongoDB connection in backend logs
- Mention data persistence across sessions
- Highlight JWT token storage in localStorage

#### Responsive Design
- Resize browser window to show mobile responsiveness
- Show Tailwind CSS styling
- Demonstrate smooth user interactions

### 5. Testing Demonstration (30 seconds)
- Run the test suite: `cd backend && python -m pytest tests/ -v`
- Show test results and coverage
- Highlight that core functionality is tested

## 🎯 Key Points to Emphasize

### User Management ✅
- Secure signup/login with JWT authentication
- Password hashing with bcrypt
- User session management

### Task Management ✅
- Full CRUD operations for tasks
- Task status tracking (pending/completed)
- Priority levels and due dates
- Real-time updates

### Labeling System ✅
- Create and manage labels with colors
- Assign multiple labels to tasks
- Filter tasks by labels
- Label-based task organization

### Technical Implementation ✅
- FastAPI backend with async operations
- Next.js frontend with TypeScript
- MongoDB for data persistence
- RESTful API design
- Modern development practices

### Code Quality ✅
- Clean, modular code structure
- Comprehensive error handling
- Type safety with TypeScript/Python
- Inline comments explaining logic
- Professional documentation

## 📝 Demo Script Notes

- **Total Duration**: ~7 minutes
- **Keep it flowing**: Don't get stuck on errors
- **Show confidence**: This is a working, production-ready app
- **Highlight innovation**: Modern tech stack and best practices
- **End strong**: Summarize the key achievements

## 🔧 Pre-Demo Setup

1. Ensure both services are running:
   ```bash
   # Terminal 1
   cd backend && python3 run.py
   
   # Terminal 2  
   cd frontend && npm run dev
   ```

2. Have test data ready:
   - Create a test user account
   - Pre-create some sample tasks and labels
   - Test all major features beforehand

3. Prepare backup plans:
   - Screenshots of key features
   - Recorded video segments
   - Live coding demonstration if needed
