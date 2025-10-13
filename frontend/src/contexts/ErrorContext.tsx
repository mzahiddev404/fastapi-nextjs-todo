"use client";

import { createContext, useContext, useState, ReactNode } from 'react';

interface ErrorContextType {
  error: Error | null;
  setError: (error: Error | null) => void;
  clearError: () => void;
}

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

interface ErrorProviderProps {
  children: ReactNode;
}

export function ErrorProvider({ children }: ErrorProviderProps) {
  const [error, setError] = useState<Error | null>(null);
  
  const clearError = () => setError(null);
  
  return (
    <ErrorContext.Provider value={{ error, setError, clearError }}>
      {children}
    </ErrorContext.Provider>
  );
}

export function useError() {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within ErrorProvider');
  }
  return context;
}
