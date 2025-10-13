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

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <LoadingSpinner size="lg" text="Loading..." />
          <p className="mt-4 text-gray-600">Setting up your workspace</p>
        </div>
      </div>
    );
  }

  // Don't render anything while redirecting
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <LoadingSpinner size="lg" text="Redirecting to login..." />
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
      await updateTaskStatus(task.id, task.status === "complete" ? "incomplete" : "complete");
    } catch (error) {
      console.error("Failed to update task status:", error);
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
    <div className="min-h-screen bg-gray-50">
      {/* Demo Banner */}
      <DemoBanner />
      
      {/* Header with user info and logout */}
      {user && <DashboardHeader user={user} onLogout={handleLogout} />}

      {/* Main content area */}
      <main id="main-content" className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8" role="main">
        <div className="px-4 py-6 sm:px-0">
              {/* Quick Actions */}
              <div className="mb-6">
                <div className="bg-white shadow rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
                    <div className="flex items-center space-x-2">
                      <Button
                        onClick={() => router.push("/tasks/status/pending")}
                        variant="secondary"
                        size="sm"
                      >
                        View Pending
                      </Button>
                      <Button
                        onClick={() => router.push("/tasks/status/completed")}
                        variant="secondary"
                        size="sm"
                      >
                        View Completed
                      </Button>
                      <Button
                        onClick={() => router.push("/profile")}
                        variant="secondary"
                        size="sm"
                      >
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
