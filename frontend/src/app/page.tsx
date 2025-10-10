"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button, Card, CardHeader, CardContent, LoadingSpinner, Alert } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";
import { TaskForm } from "@/components/TaskForm";
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

  // Don't render anything while redirecting
  if (!authLoading && !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Redirecting to login..." />
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
      await updateTaskStatus(task.id, task.status === "completed" ? "pending" : "completed");
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
  return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading your dashboard..." />
      </div>
    );
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
      {/* Header with user info and logout */}
      <header id="navigation" className="bg-white shadow" role="banner">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">TODO Dashboard</h1>
              <p className="text-gray-600">
                Welcome back, {user?.name || user?.email || "User"}!
              </p>
            </div>
            <Button
              onClick={handleLogout}
              variant="danger"
              size="sm"
              aria-label="Logout from your account"
            >
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main content area */}
      <main id="main-content" className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8" role="main">
        <div className="px-4 py-6 sm:px-0">
          {/* Task List */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Your Tasks ({tasks.length})
                </h3>
                <Button 
                  size="sm" 
                  onClick={handleCreateTask}
                  aria-label="Create a new task"
                >
                  Add Task
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {tasks.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-gray-500 mb-4">No tasks yet</div>
                  <p className="text-sm text-gray-400">Create your first task to get started!</p>
                </div>
              ) : (
                <div className="space-y-3" role="list" aria-label="Task list">
                  {tasks.map((task) => (
                    <Card
                      key={task.id}
                      className={`${
                        task.status === 'completed' 
                          ? 'bg-gray-50 border-gray-200' 
                          : 'bg-white border-gray-300'
                      }`}
                      padding="sm"
                      role="listitem"
                      aria-label={`Task: ${task.title}, Status: ${task.status}, Priority: ${task.priority}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className={`font-medium ${
                            task.status === 'completed' 
                              ? 'line-through text-gray-500' 
                              : 'text-gray-900'
                          }`}>
                            {task.title}
                          </h4>
                          {task.description && (
                            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                          )}
                          <div className="flex items-center space-x-4 mt-2">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              task.priority === 'high' 
                                ? 'bg-red-100 text-red-800'
                                : task.priority === 'medium'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-green-100 text-green-800'
                            }`}>
                              {task.priority}
                            </span>
                            {task.due_date && (
                              <span className="text-xs text-gray-500">
                                Due: {new Date(task.due_date).toLocaleDateString()}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2" role="group" aria-label={`Actions for task: ${task.title}`}>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleToggleTaskStatus(task)}
                            aria-label={`${task.status === "completed" ? "Mark as pending" : "Mark as complete"} task: ${task.title}`}
                          >
                            {task.status === "completed" ? "Mark Pending" : "Mark Complete"}
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEditTask(task)}
                            aria-label={`Edit task: ${task.title}`}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="danger"
                            size="sm"
                            onClick={() => handleDeleteTask(task)}
                            aria-label={`Delete task: ${task.title}`}
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* User info card */}
          <Card className="mt-6">
            <CardHeader>
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Account Information
              </h3>
            </CardHeader>
            <CardContent>
              <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Name</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {user?.name || "Not provided"}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Email</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user?.email}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">User ID</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user?.id}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Status</dt>
                  <dd className="mt-1 text-sm text-green-600">Authenticated</dd>
                </div>
              </dl>
            </CardContent>
          </Card>
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
