// Skeleton loading component for task list
export function TaskListSkeleton() {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      {/* Header skeleton */}
      <div className="flex justify-between items-center mb-4">
        <div className="h-6 bg-gray-200 rounded w-32 animate-pulse"></div>
        <div className="h-8 bg-gray-200 rounded w-20 animate-pulse"></div>
      </div>
      
      {/* Task items skeleton */}
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-gray-50 p-4 rounded-lg border animate-pulse">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                {/* Task title skeleton */}
                <div className="h-5 bg-gray-200 rounded w-3/4 mb-2"></div>
                {/* Task description skeleton */}
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
                {/* Priority and due date skeleton */}
                <div className="flex items-center space-x-4">
                  <div className="h-6 bg-gray-200 rounded-full w-16"></div>
                  <div className="h-4 bg-gray-200 rounded w-24"></div>
                </div>
              </div>
              {/* Action buttons skeleton */}
              <div className="flex items-center space-x-2">
                <div className="h-8 bg-gray-200 rounded w-16"></div>
                <div className="h-8 bg-gray-200 rounded w-12"></div>
                <div className="h-8 bg-gray-200 rounded w-16"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
