import { LoadingSpinner } from '@/components/ui';

// Global loading UI for the entire app
export default function GlobalLoading() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <LoadingSpinner size="lg" text="Loading your tasks..." />
    </div>
  );
}
