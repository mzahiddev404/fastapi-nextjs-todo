import { TaskListSkeleton } from './TaskListSkeleton';
import { UserInfoSkeleton } from './UserInfoSkeleton';

// Skeleton loading component for the entire dashboard
export function DashboardSkeleton() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header skeleton */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="h-6 bg-gray-200 rounded w-24 animate-pulse"></div>
            <div className="flex items-center space-x-4">
              <div className="h-8 bg-gray-200 rounded w-20 animate-pulse"></div>
              <div className="h-8 bg-gray-200 rounded w-16 animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content skeleton */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="space-y-6">
            {/* Task list skeleton */}
            <TaskListSkeleton />
            
            {/* User info skeleton */}
            <UserInfoSkeleton />
          </div>
        </div>
      </main>
    </div>
  );
}
