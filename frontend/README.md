# TODO Frontend - Next.js Application

A modern React frontend for the FastAPI-NextJS TODO application, built with Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- **User Authentication**: Signup and login with JWT tokens
- **Protected Routes**: Dashboard requires authentication
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **TypeScript**: Full type safety throughout the application
- **shadcn/ui Components**: Modern, accessible UI components
- **React Context**: State management with React Context API
- **API Integration**: Seamless communication with FastAPI backend

## Getting Started

### Prerequisites

- Node.js 18+ 
- Backend server running on http://localhost:8000

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication pages
│   │   │   ├── login/         # Login page
│   │   │   └── signup/        # Signup page
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Dashboard (protected)
│   └── lib/
│       └── apiClient.ts       # API client utilities
├── package.json
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Authentication Flow

1. **Signup**: Create new account → Store JWT token → Redirect to dashboard
2. **Login**: Enter credentials → Store JWT token → Redirect to dashboard  
3. **Dashboard**: Protected route that validates token and shows user info
4. **Logout**: Clear token → Redirect to login

## API Integration

The frontend communicates with the FastAPI backend through a centralized API client (`src/lib/apiClient.ts`) that handles:

- **Authentication token management** - Automatic token storage and retrieval
- **Request/response interceptors** - Centralized error handling and logging
- **Error handling** - Consistent error processing across all requests
- **Automatic token refresh** - Seamless token renewal on 401 errors

### Available Endpoints

**Authentication:**
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/demo` - Demo session creation
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/refresh` - Refresh JWT token

**Tasks:**
- `GET /api/v1/tasks` - List all tasks (with optional status filter)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/status` - Update task status
- `GET /api/v1/tasks/stats` - Get task statistics

**Labels:**
- `GET /api/v1/labels` - List all labels
- `POST /api/v1/labels` - Create new label
- `GET /api/v1/labels/{id}` - Get specific label
- `PUT /api/v1/labels/{id}` - Update label
- `DELETE /api/v1/labels/{id}` - Delete label

## Development Notes

- Uses `localStorage` for token storage (development only)
- All API calls include proper error handling
- Responsive design works on mobile and desktop
- TypeScript provides compile-time type checking
