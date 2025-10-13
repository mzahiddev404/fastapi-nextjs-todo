"use client";

import { useParams, useRouter } from "next/navigation";
import { useMemo } from "react";
import { Button, Alert, LoadingSpinner } from "@/components/ui";
import { useTasks } from "@/hooks/useTasks";
import { useLabels } from "@/hooks/useLabels";
import { useAuth } from "@/hooks/useAuth";
import { TaskList } from "@/components/TaskList";
import { Task } from "@/types";

// Task label filtering page with dynamic route parameter
export default function TaskLabelPage() {
  const params = useParams();
  const router = useRouter();
  const labelName = params.label as string;
  const { tasks, isLoading: tasksLoading, error: tasksError, updateTaskStatus, deleteTask } = useTasks();
  const { labels, isLoading: labelsLoading, error: labelsError } = useLabels();
  const { user } = useAuth();

  // Find the label by name
  const label = labels.find(l => l.name.toLowerCase() === labelName.toLowerCase());

  // Filter tasks by label
  const filteredTasks = useMemo(() => {
    if (!label) return [];
    return tasks.filter(task => 
      task.labels && task.labels.some(taskLabel => taskLabel.id === label.id)
    );
  }, [tasks, label]);

  // Handle task actions
  const handleEditTask = (task: Task) => {
    router.push(`/tasks/${task.id}`);
  };

  const handleToggleTaskStatus = async (task: Task) => {
    try {
      const newStatus = task.status === "completed" ? "pending" : "completed";
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
  if (tasksLoading || labelsLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading tasks..." />
      </div>
    );
  }

  // Error state
  if (tasksError || labelsError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full">
          <Alert variant="error" className="mb-4">
            <h2 className="text-lg font-semibold mb-2">Error Loading Tasks</h2>
            <p className="text-sm">
              {tasksError?.message || labelsError?.message || "Failed to load tasks. Please try again."}
            </p>
          </Alert>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Label not found
  if (!label) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full text-center">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Label Not Found
            </h1>
            <p className="text-gray-600">
              The label "{labelName}" doesn't exist or has been deleted.
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
              <h1 className="text-xl font-semibold text-gray-900">
                Tasks with Label: {label.name}
              </h1>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {label.name}
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
          {/* Label filter info */}
          <div className="mb-6">
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-medium text-gray-900">
                    Tasks with Label: {label.name}
                  </h2>
                  <p className="text-sm text-gray-500">
                    {filteredTasks.length} task{filteredTasks.length !== 1 ? "s" : ""} found
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    onClick={() => router.push("/tasks/status/pending")}
                    variant="secondary"
                    size="sm"
                  >
                    Pending Tasks
                  </Button>
                  <Button
                    onClick={() => router.push("/tasks/status/completed")}
                    variant="secondary"
                    size="sm"
                  >
                    Completed Tasks
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
                    d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No tasks with this label
              </h3>
              <p className="text-gray-500 mb-4">
                There are no tasks with the label "{label.name}" at the moment.
              </p>
              <Button onClick={handleCreateTask} variant="primary">
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
