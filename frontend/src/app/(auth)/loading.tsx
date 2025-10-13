import { LoadingSpinner } from '@/components/ui';

// Loading UI for authentication pages
export default function AuthLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            My TODO App
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Signing you in...
          </p>
        </div>
        <div className="flex justify-center">
          <LoadingSpinner size="md" text="Loading..." />
        </div>
      </div>
    </div>
  );
}
