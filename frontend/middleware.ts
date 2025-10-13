import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Middleware for route protection and authentication
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Get token from cookies (more secure than localStorage for SSR)
  const token = request.cookies.get('todo_token')?.value;
  
  // Define protected routes that require authentication
  const protectedRoutes = [
    '/',
    '/profile',
    '/tasks',
  ];
  
  // Define public routes that don't require authentication
  const publicRoutes = [
    '/auth/login',
    '/auth/signup',
  ];
  
  // Check if the current path is protected
  const isProtectedRoute = protectedRoutes.some(route => 
    pathname === route || pathname.startsWith(route + '/')
  );
  
  // Check if the current path is public
  const isPublicRoute = publicRoutes.some(route => 
    pathname === route || pathname.startsWith(route + '/')
  );
  
  // If accessing a protected route without a token, redirect to login
  if (isProtectedRoute && !token) {
    const loginUrl = new URL('/auth/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  // If accessing a public route with a token, redirect to dashboard
  if (isPublicRoute && token) {
    return NextResponse.redirect(new URL('/', request.url));
  }
  
  // Allow the request to continue
  return NextResponse.next();
}

// Configure which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
