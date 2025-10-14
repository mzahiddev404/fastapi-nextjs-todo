"use client";

import { useParams, useRouter } from "next/navigation";
import { useMemo } from "react";
import { Button, Alert, LoadingSpinner } from "@/components/ui";
import { useTasks } from "@/hooks/useTasks";
import { useAuth } from "@/hooks/useAuth";
import { TaskList } from "@/components/TaskList";
import { Task } from "@/types";

// Task status filtering page with dynamic route parameter
export default function TaskStatusPage() {
  const params = useParams();
  const router = useRouter();
  const status = params.status as string;
  const { tasks, isLoading, error, updateTaskStatus, deleteTask } = useTasks();
  const { user } = useAuth();

  // Validate status parameter
  const validStatuses = ["incomplete", "complete"];
  const isValidStatus = validStatuses.includes(status);

  // Filter tasks by status
  const filteredTasks = useMemo(() => {
    if (!isValidStatus) return [];
    return tasks.filter(task => task.status === status);
  }, [tasks, status, isValidStatus]);

  // Handle task actions
  const handleEditTask = (task: Task) => {
    router.push(`/tasks/${task.id}`);
  };

  const handleToggleTaskStatus = async (task: Task) => {
    try {
      const newStatus = task.status === "complete" ? "incomplete" : "complete";
      await updateTaskStatus(task.id, newStatus);
    } catch (error) {
      console.error("Failed to update task status:", error);
    }
  };

  const handleDeleteTask = async (task: Task) => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      await deleteTask(task.id);
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  const handleCreateTask = () => {
    router.push("/");
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading tasks..." />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full">
          <Alert variant="error" className="mb-4">
            <h2 className="text-lg font-semibold mb-2">Error Loading Tasks</h2>
            <p className="text-sm">
              {error.message || "Failed to load tasks. Please try again."}
            </p>
          </Alert>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Invalid status
  if (!isValidStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full text-center">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Invalid Status
            </h1>
            <p className="text-gray-600">
              The status "{status}" is not valid. Please use "incomplete" or "complete".
            </p>
          </div>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  const statusDisplayName = status === "complete" ? "Completed" : "Pending";
  const statusColor = status === "complete" ? "green" : "yellow";

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="secondary"
                onClick={() => router.push("/")}
                className="flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back to Dashboard</span>
              </Button>
              <h1 className="text-xl font-semibold text-gray-900">
                {statusDisplayName} Tasks
              </h1>
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  statusColor === "green"
                    ? "bg-green-100 text-green-800"
                    : "bg-yellow-100 text-yellow-800"
                }`}
              >
                {statusDisplayName}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">
                {user?.username || "User"}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Status filter info */}
          <div className="mb-6">
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-medium text-gray-900">
                    {statusDisplayName} Tasks
                  </h2>
                  <p className="text-sm text-gray-500">
                    {filteredTasks.length} task{filteredTasks.length !== 1 ? "s" : ""} found
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    onClick={() => router.push("/tasks/status/incomplete")}
                    variant="secondary"
                    size="sm"
                  >
                    Pending
                  </Button>
                  <Button
                    onClick={() => router.push("/tasks/status/complete")}
                    variant="secondary"
                    size="sm"
                  >
                    Completed
                  </Button>
                </div>
              </div>
            </div>
          </div>

          {/* Task list */}
          {filteredTasks.length === 0 ? (
            <div className="bg-white shadow rounded-lg p-8 text-center">
              <div className="mb-4">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No {statusDisplayName.toLowerCase()} tasks
              </h3>
              <p className="text-gray-500 mb-4">
                {status === "incomplete"
                  ? "You don't have any pending tasks at the moment."
                  : "You haven't completed any tasks yet."}
              </p>
              <Button onClick={handleCreateTask} >
                Create New Task
              </Button>
            </div>
          ) : (
            <TaskList
              tasks={filteredTasks}
              onEditTask={handleEditTask}
              onToggleTaskStatus={handleToggleTaskStatus}
              onDeleteTask={handleDeleteTask}
              onCreateTask={handleCreateTask}
            />
          )}
        </div>
      </main>
    </div>
  );
}
