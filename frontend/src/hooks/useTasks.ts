// Custom hook for task management using SWR
import useSWR, { mutate } from "swr";
import { Task, TaskCreate, TaskUpdate, TaskStats } from "@/types";
import { api } from "@/lib/apiClient";

// Fetcher function for SWR
const fetcher = (url: string) => api.get<Task[]>(url);

export function useTasks() {
  // Fetch all tasks
  const { data: tasks, error, isLoading, mutate } = useSWR(
    "/api/v1/tasks",
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 30000, // Cache for 30 seconds
    }
  );

  // Create a new task
  const createTask = async (taskData: TaskCreate) => {
    try {
      const newTask = await api.post<Task>("/api/v1/tasks", taskData);
      mutate(); // Revalidate tasks list
      return newTask;
    } catch (error) {
      throw error;
    }
  };

  // Update a task
  const updateTask = async (taskId: string, taskData: TaskUpdate) => {
    try {
      const updatedTask = await api.put<Task>(`/api/v1/tasks/${taskId}`, taskData);
      mutate(); // Revalidate tasks list
      return updatedTask;
    } catch (error) {
      throw error;
    }
  };

  // Update task status
  const updateTaskStatus = async (taskId: string, status: "pending" | "completed") => {
    try {
      const updatedTask = await api.patch<Task>(`/api/v1/tasks/${taskId}/status`, { status });
      mutate(); // Revalidate tasks list
      return updatedTask;
    } catch (error) {
      throw error;
    }
  };

  // Delete a task
  const deleteTask = async (taskId: string) => {
    try {
      await api.delete(`/api/v1/tasks/${taskId}`);
      mutate(); // Revalidate tasks list
    } catch (error) {
      throw error;
    }
  };

  // Get task statistics
  const getTaskStats = async (): Promise<TaskStats> => {
    try {
      const stats = await api.get<TaskStats>("/api/v1/tasks/stats");
      return stats;
    } catch (error) {
      throw error;
    }
  };

  return {
    tasks: tasks || [],
    isLoading,
    error,
    createTask,
    updateTask,
    updateTaskStatus,
    deleteTask,
    getTaskStats,
    mutate,
  };
}
