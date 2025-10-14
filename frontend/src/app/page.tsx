"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { Button, LoadingSpinner, Alert } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";
import { useLabels } from "@/hooks/useLabels";
import { TaskForm } from "@/components/TaskForm";
import { TaskList } from "@/components/TaskList";
import { UserInfo } from "@/components/UserInfo";
import { DashboardHeader } from "@/components/DashboardHeader";
import { DashboardSkeleton } from "@/components/skeletons";
import { Task } from "@/types";

// Main dashboard page - protected route that shows user info and task list
export default function Home() {
  const router = useRouter();
  const { user, isLoading: authLoading, error: authError, isAuthenticated, logout } = useAuth();
  const { tasks, isLoading: tasksLoading, error: tasksError, updateTaskStatus, deleteTask } = useTasks();
  const { labels } = useLabels();
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isMounted, setIsMounted] = useState(false);
  const [hasToken, setHasToken] = useState(false);
  const [selectedLabelFilter, setSelectedLabelFilter] = useState<string | null>(null);

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

  // Filter tasks based on selected label (must be called before any conditional returns)
  const filteredTasks = useMemo(() => {
    if (!selectedLabelFilter) {
      return tasks;
    }
    return tasks.filter(task => task.labels && task.labels.includes(selectedLabelFilter));
  }, [tasks, selectedLabelFilter]);

  // Get label details by ID
  const getLabelById = (labelId: string) => {
    return labels.find(label => label.id === labelId);
  };

  // Show loading while checking authentication or during SSR
  // If there's an auth error and we have a token, clear it and redirect to login
  if (isMounted && authError && hasToken) {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('todo_token');
    }
    router.push("/auth/login");
    return null;
  }

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

  // Handle task status toggle (checkbox) - marks task as complete or incomplete
  const handleToggleTaskStatus = async (task: Task) => {
    try {
      const newStatus = task.status === "complete" ? "incomplete" : "complete";
      await updateTaskStatus(task.id, newStatus);
    } catch (error) {
      console.error("Failed to update task status:", error);
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
    <div className="min-h-screen relative overflow-hidden">
      {/* Floating particles background */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-10 w-32 h-32 bg-yellow-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '3s' }}></div>
        <div className="absolute top-1/3 right-20 w-40 h-40 bg-pink-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-36 h-36 bg-cyan-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '5s', animationDelay: '2s' }}></div>
        <div className="absolute bottom-1/4 right-1/4 w-28 h-28 bg-purple-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '6s', animationDelay: '0.5s' }}></div>
      </div>
      
      {/* Header with user info and logout */}
      {user && <DashboardHeader user={user} onLogout={handleLogout} />}

      {/* Main content area */}
      <main id="main-content" className="max-w-7xl mx-auto py-4 sm:py-6 md:py-8 px-3 sm:px-6 lg:px-8" role="main">
        <div className="space-y-4 sm:space-y-6 md:space-y-8">
              {/* Quick Actions */}
              <div className="transform hover:scale-[1.02] transition-transform duration-300">
                <div className="bg-white/95 backdrop-blur-xl shadow-[0_20px_70px_-10px_rgba(79,70,229,0.4)] rounded-2xl p-4 sm:p-5 md:p-6 border-2 border-indigo-200/50 relative overflow-hidden group hover:border-indigo-300 hover:shadow-[0_25px_80px_-15px_rgba(79,70,229,0.5)] transition-all duration-500">
                  {/* Animated gradient overlay */}
                  <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/60 via-purple-100/40 to-pink-100/60 opacity-60"></div>
                  {/* Shine effect */}
                  <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  <div className="relative z-10">
                  <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3 sm:gap-4">
                    <div className="w-full lg:w-auto">
                      <h3 className="text-lg sm:text-xl font-bold text-gray-900 mb-1">Quick Actions</h3>
                      <p className="text-xs sm:text-sm text-gray-600 hidden sm:block">Jump to your most used features</p>
                    </div>
                    <div className="flex items-center gap-2 sm:gap-3 flex-wrap w-full lg:w-auto">
                      <Button
                        onClick={() => router.push("/tasks/status/incomplete")}
                        variant="secondary"
                        size="sm"
                        className="flex-1 sm:flex-none bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200 text-xs sm:text-sm"
                      >
                        <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span className="hidden xs:inline">View </span>Pending
                      </Button>
                      <Button
                        onClick={() => router.push("/tasks/status/complete")}
                        variant="secondary"
                        size="sm"
                        className="flex-1 sm:flex-none bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200 text-xs sm:text-sm"
                      >
                        <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span className="hidden xs:inline">View </span>Complete
                      </Button>
                      <Button
                        onClick={() => router.push("/profile")}
                        variant="secondary"
                        size="sm"
                        className="flex-1 sm:flex-none bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white border-0 shadow-md hover:shadow-lg transition-all duration-200 text-xs sm:text-sm"
                      >
                        <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        Profile
                      </Button>
                    </div>
                  </div>
                  </div>
                </div>
              </div>

              {/* Label Filters */}
              {labels.length > 0 && (
                <div className="transform hover:scale-[1.02] transition-transform duration-300">
                  <div className="bg-white/95 backdrop-blur-xl shadow-[0_20px_70px_-10px_rgba(168,85,247,0.4)] rounded-2xl p-4 sm:p-5 border-2 border-purple-200/50 relative overflow-hidden group hover:border-purple-300 hover:shadow-[0_25px_80px_-15px_rgba(168,85,247,0.5)] transition-all duration-500">
                    {/* Animated gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-100/60 via-pink-100/40 to-rose-100/60 opacity-60"></div>
                    {/* Shine effect */}
                    <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                    <div className="relative z-10">
                    <div className="flex flex-col space-y-3 sm:space-y-4">
                      <div className="flex items-center gap-2">
                        <svg className="w-4 h-4 sm:w-5 sm:h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                        </svg>
                        <h3 className="text-sm sm:text-base font-semibold text-gray-900">Filter by Label</h3>
                      </div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          onClick={() => setSelectedLabelFilter(null)}
                          className={`px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-all duration-200 ${
                            selectedLabelFilter === null
                              ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          <span className="hidden xs:inline">All </span>Tasks
                          <span className="ml-1.5 sm:ml-2 inline-flex items-center justify-center px-1.5 sm:px-2 py-0.5 rounded-full text-xs bg-white/20">
                            {tasks.length}
                          </span>
                        </button>
                        {labels.map((label) => (
                          <button
                            key={label.id}
                            onClick={() => setSelectedLabelFilter(label.id)}
                            className={`px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all duration-200 ${
                              selectedLabelFilter === label.id
                                ? 'shadow-lg scale-105'
                                : 'hover:scale-105 shadow-sm'
                            }`}
                            style={{
                              backgroundColor: selectedLabelFilter === label.id ? label.color : `${label.color}20`,
                              color: selectedLabelFilter === label.id ? '#fff' : label.color,
                              borderWidth: '2px',
                              borderColor: label.color,
                            }}
                          >
                            <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full inline-block mr-1.5 sm:mr-2" style={{ backgroundColor: selectedLabelFilter === label.id ? '#fff' : label.color }}></span>
                            {label.name}
                            <span className="ml-1.5 sm:ml-2 inline-flex items-center justify-center px-1.5 sm:px-2 py-0.5 rounded-full text-xs" style={{ backgroundColor: selectedLabelFilter === label.id ? 'rgba(255,255,255,0.3)' : `${label.color}30` }}>
                              {tasks.filter(t => t.labels && t.labels.includes(label.id)).length}
                            </span>
                          </button>
                        ))}
                      </div>
                    </div>
                    {selectedLabelFilter && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-xs sm:text-sm text-gray-600">
                          Showing <span className="font-semibold text-gray-900">{filteredTasks.length}</span> task{filteredTasks.length !== 1 ? 's' : ''} with{' '}
                          <span className="font-semibold" style={{ color: getLabelById(selectedLabelFilter)?.color }}>
                            {getLabelById(selectedLabelFilter)?.name}
                          </span>
                        </p>
                      </div>
                    )}
                    </div>
                  </div>
                </div>
              )}

          {/* Task List */}
          <TaskList
            tasks={filteredTasks}
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
