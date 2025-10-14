"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button, LoadingSpinner, Alert } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";
import { TaskForm } from "@/components/TaskForm";
import { TaskList } from "@/components/TaskList";
import { UserInfo } from "@/components/UserInfo";
import { DashboardHeader } from "@/components/DashboardHeader";
import { DashboardSkeleton } from "@/components/skeletons";
import { DemoBanner } from "@/components/DemoBanner";
import { Task } from "@/types";

// Main dashboard page - protected route that shows user info and task list
export default function Home() {
  const router = useRouter();
  const { user, isLoading: authLoading, error: authError, isAuthenticated, logout } = useAuth();
  const { tasks, isLoading: tasksLoading, error: tasksError, updateTaskStatus, deleteTask } = useTasks();
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isMounted, setIsMounted] = useState(false);
  const [hasToken, setHasToken] = useState(false);

  // Check if component is mounted and if token exists (client-side only)
  useEffect(() => {
    setIsMounted(true);
    if (typeof window !== 'undefined') {
      setHasToken(!!localStorage.getItem('todo_token'));
    }
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    // Only redirect if we're done loading AND there's no user AND no token
    if (isMounted && !authLoading && !isAuthenticated && !hasToken) {
      router.push("/auth/login");
    }
  }, [isMounted, authLoading, isAuthenticated, hasToken, router]);

  // Show loading while checking authentication or during SSR
  if (!isMounted || authLoading || (hasToken && !user && !authError)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <LoadingSpinner size="lg" text="Loading..." />
          <p className="mt-4 text-gray-600">Setting up your workspace</p>
        </div>
      </div>
    );
  }

  // Don't render anything while redirecting (only if no token and not authenticated)
  if (!isAuthenticated && !hasToken) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <LoadingSpinner size="lg" text="Loading..." />
          <p className="mt-4 text-gray-600">Please sign in to continue</p>
        </div>
      </div>
    );
  }

  const isLoading = authLoading || tasksLoading;
  const error = authError || tasksError;

  // Handle user logout
  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  // Handle task actions
  const handleCreateTask = () => {
    setEditingTask(null);
    setShowTaskForm(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleToggleTaskStatus = async (task: Task) => {
    try {
      console.log("🔄 Toggling task status:", task.id, "from", task.status, "to", task.status === "complete" ? "incomplete" : "complete");
      const newStatus = task.status === "complete" ? "incomplete" : "complete";
      await updateTaskStatus(task.id, newStatus);
      console.log("✅ Task status updated successfully");
    } catch (error) {
      console.error("❌ Failed to update task status:", error);
      alert("Failed to update task status. Please try again.");
    }
  };

  const handleDeleteTask = async (task: Task) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await deleteTask(task.id);
      } catch (error) {
        console.error("Failed to delete task:", error);
      }
    }
  };

  const handleTaskFormClose = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <Alert variant="error" className="mb-4">
            {error instanceof Error ? error.message : String(error)}
          </Alert>
          <Button
            onClick={() => window.location.reload()}
            className="w-full"
            size="lg"
          >
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Demo Banner */}
      <DemoBanner />
      
      {/* Header with user info and logout */}
      {user && <DashboardHeader user={user} onLogout={handleLogout} />}

      {/* Main content area */}
      <main id="main-content" className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8" role="main">
        <div className="px-4 py-6 sm:px-0">
              {/* Quick Actions */}
              <div className="mb-8">
                <div className="bg-white/80 backdrop-blur-sm shadow-lg shadow-indigo-100/50 rounded-2xl p-6 border border-indigo-100/50">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 mb-1">Quick Actions</h3>
                      <p className="text-sm text-gray-600">Jump to your most used features</p>
                    </div>
                    <div className="flex items-center gap-3 flex-wrap">
                      <Button
                        onClick={() => router.push("/tasks/status/incomplete")}
                        variant="secondary"
                        size="sm"
                        className="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        View Pending
                      </Button>
                      <Button
                        onClick={() => router.push("/tasks/status/complete")}
                        variant="secondary"
                        size="sm"
                        className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        View Completed
                      </Button>
                      <Button
                        onClick={() => router.push("/profile")}
                        variant="secondary"
                        size="sm"
                        className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        My Profile
                      </Button>
                    </div>
                  </div>
                </div>
              </div>

          {/* Task List */}
          <TaskList
            tasks={tasks}
            onEditTask={handleEditTask}
            onToggleTaskStatus={handleToggleTaskStatus}
            onDeleteTask={handleDeleteTask}
            onCreateTask={handleCreateTask}
          />

          {/* User info card */}
          {user && <UserInfo user={user} />}
        </div>
      </main>

      {/* Task Form Modal */}
      {showTaskForm && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          role="dialog"
          aria-modal="true"
          aria-labelledby="task-form-title"
        >
          <div className="w-full max-w-2xl">
            <TaskForm
              task={editingTask || undefined}
              onClose={handleTaskFormClose}
              onSuccess={() => {
                // Task will be automatically refreshed by SWR
              }}
            />
          </div>
        </div>
      )}
      
    </div>
  );
}
