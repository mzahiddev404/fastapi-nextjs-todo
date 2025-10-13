"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Button, Alert, LoadingSpinner } from "@/components/ui";
import { useTasks } from "@/hooks/useTasks";
import { useAuth } from "@/hooks/useAuth";
import { Task } from "@/types";

// Task detail page with dynamic route parameter
export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const taskId = params.id as string;
  const { tasks, isLoading, error, updateTaskStatus, deleteTask } = useTasks();
  const { user } = useAuth();
  const [isDeleting, setIsDeleting] = useState(false);

  // Find the specific task
  const task = tasks.find(t => t.id === taskId);

  // Redirect to dashboard if task not found
  useEffect(() => {
    if (!isLoading && !error && tasks.length > 0 && !task) {
      router.push("/");
    }
  }, [isLoading, error, tasks, task, router]);

  // Handle task status toggle
  const handleToggleStatus = async () => {
    if (!task) return;
    
    try {
      const newStatus = task.status === "complete" ? "incomplete" : "complete";
      await updateTaskStatus(task.id, newStatus);
    } catch (error) {
      console.error("Failed to update task status:", error);
    }
  };

  // Handle task deletion
  const handleDelete = async () => {
    if (!task) return;
    
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTask(task.id);
      router.push("/");
    } catch (error) {
      console.error("Failed to delete task:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  // Handle edit task
  const handleEdit = () => {
    router.push(`/?edit=${taskId}`);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading task..." />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full">
          <Alert variant="error" className="mb-4">
            <h2 className="text-lg font-semibold mb-2">Error Loading Task</h2>
            <p className="text-sm">
              {error.message || "Failed to load task details. Please try again."}
            </p>
          </Alert>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Task not found
  if (!task) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full text-center">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Task Not Found
            </h1>
            <p className="text-gray-600">
              The task you're looking for doesn't exist or has been deleted.
            </p>
          </div>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

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
              <h1 className="text-xl font-semibold text-gray-900">Task Details</h1>
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
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    {task.title}
                  </h2>
                  <div className="flex items-center space-x-4">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.status === "complete"
                          ? "bg-green-100 text-green-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {task.status === "complete" ? "Completed" : "Pending"}
                    </span>
                    <span className="text-sm text-gray-500">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </span>
                    {task.deadline && (
                      <span className="text-sm text-gray-500">
                        Due: {new Date(task.deadline).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    onClick={handleToggleStatus}
                    variant="secondary"
                    size="sm"
                  >
                    {task.status === "complete" ? "Mark Pending" : "Mark Complete"}
                  </Button>
                  <Button
                    onClick={handleEdit}
                    variant="secondary"
                    size="sm"
                  >
                    Edit
                  </Button>
                  <Button
                    onClick={handleDelete}
                    variant="destructive"
                    size="sm"
                    disabled={isDeleting}
                  >
                    {isDeleting ? "Deleting..." : "Delete"}
                  </Button>
                </div>
              </div>
            </div>

            <div className="px-6 py-4">
              {task.description && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
                </div>
              )}

              {task.labels && task.labels.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Labels</h3>
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {task.labels.length} label(s) assigned
                    </span>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Task Information</h3>
                  <dl className="space-y-2">
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Status</dt>
                      <dd className="text-sm text-gray-900">
                        {task.status === "complete" ? "Completed" : "Pending"}
                      </dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Priority</dt>
                      <dd className="text-sm text-gray-900">
                        {task.priority || "Normal"}
                      </dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Created</dt>
                      <dd className="text-sm text-gray-900">
                        {new Date(task.created_at).toLocaleString()}
                      </dd>
                    </div>
                    {task.updated_at && (
                      <div>
                        <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                        <dd className="text-sm text-gray-900">
                          {new Date(task.updated_at).toLocaleString()}
                        </dd>
                      </div>
                    )}
                  </dl>
                </div>

                {task.deadline && (
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Due Date</h3>
                    <div className="text-sm text-gray-900">
                      {new Date(task.deadline).toLocaleDateString("en-US", {
                        weekday: "long",
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </div>
                    {new Date(task.deadline) < new Date() && task.status !== "complete" && (
                      <div className="mt-2 text-sm text-red-600 font-medium">
                        Overdue
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
