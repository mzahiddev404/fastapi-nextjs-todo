// Skeleton loading component for user info
export function UserInfoSkeleton() {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
      {/* User info header */}
      <div className="flex items-center space-x-3 mb-4">
        <div className="h-12 w-12 bg-gray-200 rounded-full"></div>
        <div className="flex-1">
          <div className="h-5 bg-gray-200 rounded w-32 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-24"></div>
        </div>
      </div>
      
      {/* User stats skeleton */}
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center">
          <div className="h-8 bg-gray-200 rounded w-12 mx-auto mb-1"></div>
          <div className="h-4 bg-gray-200 rounded w-16 mx-auto"></div>
        </div>
        <div className="text-center">
          <div className="h-8 bg-gray-200 rounded w-12 mx-auto mb-1"></div>
          <div className="h-4 bg-gray-200 rounded w-20 mx-auto"></div>
        </div>
      </div>
    </div>
  );
}
