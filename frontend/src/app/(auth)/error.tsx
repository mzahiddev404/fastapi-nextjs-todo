"use client";

import { useEffect } from 'react';
import { Button, Alert } from '@/components/ui';

// Error boundary for authentication pages
export default function AuthError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Auth error:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Authentication Error
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Something went wrong with the authentication process
          </p>
        </div>
        
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <Alert variant="error" className="mb-4">
            {error.message || 'Authentication failed'}
          </Alert>
          
          <div className="space-y-3">
            <Button onClick={reset} className="w-full">
              Try Again
            </Button>
            <Button 
              variant="secondary" 
              onClick={() => window.location.href = '/'}
              className="w-full"
            >
              Go Home
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
