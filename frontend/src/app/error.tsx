"use client";

import { useEffect } from 'react';
import { Button, Alert } from '@/components/ui';

// Global error boundary for the entire app
export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to console (in production, send to error reporting service)
    console.error('Global error:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md w-full text-center">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Oops! Something went wrong
          </h1>
          <p className="text-gray-600">
            We're sorry, but something unexpected happened. Please try again.
          </p>
        </div>
        
        <Alert variant="error" className="mb-6">
          {error.message || 'An unexpected error occurred'}
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
  );
}
