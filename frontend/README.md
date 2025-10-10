# TODO Frontend - Next.js Application

A modern React frontend for the FastAPI-NextJS TODO application, built with Next.js 15, TypeScript, and Tailwind CSS.

## Features

- **User Authentication**: Signup and login with JWT tokens
- **Protected Routes**: Dashboard requires authentication
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **TypeScript**: Full type safety throughout the application
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

The frontend communicates with the FastAPI backend using:
- **Base URL**: http://localhost:8000
- **Authentication**: JWT tokens stored in localStorage
- **Endpoints**: 
  - `POST /api/v1/auth/signup` - User registration
  - `POST /api/v1/auth/login` - User login
  - `GET /api/v1/auth/me` - Get current user

## Development Notes

- Uses `localStorage` for token storage (development only)
- All API calls include proper error handling
- Responsive design works on mobile and desktop
- TypeScript provides compile-time type checking
