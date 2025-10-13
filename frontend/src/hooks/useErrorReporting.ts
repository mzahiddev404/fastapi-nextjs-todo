import { useError } from '@/contexts/ErrorContext';

// Hook for error reporting and management
export function useErrorReporting() {
  const { setError } = useError();
  
  const reportError = (error: Error, context?: string) => {
    console.error(`Error in ${context || 'unknown context'}:`, error);
    
    // In production, send to error reporting service
    if (process.env.NODE_ENV === 'production') {
      // Example: Sentry.captureException(error, { tags: { context } });
      // Example: LogRocket.captureException(error);
    }
    
    setError(error);
  };
  
  const reportAsyncError = async (
    asyncFn: () => Promise<any>,
    context?: string,
    fallbackMessage?: string
  ) => {
    try {
      return await asyncFn();
    } catch (error) {
      const errorObj = error instanceof Error 
        ? error 
        : new Error(fallbackMessage || 'An unexpected error occurred');
      
      reportError(errorObj, context);
      throw errorObj;
    }
  };
  
  return { 
    reportError, 
    reportAsyncError 
  };
}
