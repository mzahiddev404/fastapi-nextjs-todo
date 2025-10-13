"use client";

import { useLoading } from '@/contexts/LoadingContext';
import { LoadingSpinner } from '@/components/ui';

// Global loading indicator that appears at the top of the page
export function GlobalLoading() {
  const { isLoading, loadingMessage } = useLoading();
  
  if (!isLoading) return null;
  
  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b">
      <div className="flex items-center justify-center py-2">
        <LoadingSpinner size="sm" text={loadingMessage} />
      </div>
    </div>
  );
}
