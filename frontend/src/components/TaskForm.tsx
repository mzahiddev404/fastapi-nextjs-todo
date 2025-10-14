"use client";

// TaskForm component for creating and editing tasks
import { useState } from "react";
import { Task, TaskCreate, TaskUpdate, Label } from "@/types";
import { useTasks } from "@/hooks/useTasks";
import { useLabels } from "@/hooks/useLabels";
import { Button, Input, Card, CardHeader, CardContent, Alert } from "@/components/ui";

interface TaskFormProps {
  task?: Task;
  onClose: () => void;
  onSuccess?: () => void;
}

export function TaskForm({ task, onClose, onSuccess }: TaskFormProps) {
  // Convert ISO date to YYYY-MM-DD format for date input
  const formatDateForInput = (dateString?: string) => {
    if (!dateString) return "";
    try {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    } catch {
      return "";
    }
  };

  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState<"low" | "medium" | "high">(task?.priority || "medium");
  const [dueDate, setDueDate] = useState(formatDateForInput(task?.deadline));
  const [selectedLabels, setSelectedLabels] = useState<string[]>(task?.labels || []);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const { createTask, updateTask } = useTasks();
  const { labels } = useLabels();

  const isEditing = !!task;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // Convert date to ISO format for backend
      const deadlineISO = dueDate ? new Date(dueDate).toISOString() : new Date().toISOString();
      
      const taskData: TaskCreate | TaskUpdate = {
        title,
        description: description || undefined,
        priority,
        deadline: deadlineISO,  // Required field in ISO format
        labels: selectedLabels.length > 0 ? selectedLabels : undefined,
      };

      if (isEditing) {
        await updateTask(task.id, taskData as TaskUpdate);
      } else {
        await createTask(taskData as TaskCreate);
      }

      onSuccess?.();
      onClose();
    } catch (err) {
      console.error("Task save error:", err);
      setError(err instanceof Error ? err.message : "Failed to save task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLabelToggle = (labelId: string) => {
    setSelectedLabels(prev =>
      prev.includes(labelId)
        ? prev.filter(id => id !== labelId)
        : [...prev, labelId]
    );
  };

  // Common task suggestions - modern, relevant tasks for today's lifestyle
  const taskSuggestions = [
    { emoji: "🛒", text: "Buy groceries" },
    { emoji: "📞", text: "Make a call" },
    { emoji: "📅", text: "Schedule appointment" },
    { emoji: "💊", text: "Take medicine" },
    { emoji: "🚫", text: "Get off social media" },
    { emoji: "👨‍👩‍👧", text: "Spend time with family" },
    { emoji: "🏋️", text: "Exercise/Workout" },
    { emoji: "💧", text: "Drink water" },
    { emoji: "🧘", text: "Meditate" },
    { emoji: "📚", text: "Read a book" },
    { emoji: "💼", text: "Work meeting" },
    { emoji: "🌙", text: "Sleep early tonight" },
  ];

  const handleSuggestionClick = (suggestionText: string) => {
    setTitle(suggestionText);
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <h3 id="task-form-title" className="text-lg font-medium text-gray-900">
          {isEditing ? "Edit Task" : "Create New Task"}
        </h3>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Input
              label="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title"
              required
            />
            {/* Task Suggestions - only show when creating new task */}
            {!isEditing && !title && (
              <div className="mt-3 p-3 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 rounded-xl border border-indigo-100">
                <p className="text-xs font-semibold text-indigo-900 mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Quick suggestions:
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                  {taskSuggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => handleSuggestionClick(suggestion.text)}
                      className="px-2.5 py-2 bg-white hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 border border-gray-200 hover:border-indigo-300 rounded-lg text-xs font-medium text-gray-700 hover:text-indigo-900 transition-all duration-200 hover:scale-105 hover:shadow-md text-left flex items-center gap-2"
                    >
                      <span className="text-base flex-shrink-0">{suggestion.emoji}</span>
                      <span className="truncate">{suggestion.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter task description (optional)"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              rows={3}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as "low" | "medium" | "high")}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Due Date <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
          </div>

          {labels.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Labels
              </label>
              <div className="flex flex-wrap gap-2">
                {labels.map((label) => (
                  <button
                    key={label.id}
                    type="button"
                    onClick={() => handleLabelToggle(label.id)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      selectedLabels.includes(label.id)
                        ? "bg-indigo-100 text-indigo-800 border-2 border-indigo-300"
                        : "bg-gray-100 text-gray-700 border-2 border-transparent hover:bg-gray-200"
                    }`}
                    style={{
                      backgroundColor: selectedLabels.includes(label.id) ? label.color + "20" : undefined,
                      borderColor: selectedLabels.includes(label.id) ? label.color : undefined,
                    }}
                  >
                    {label.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {error && (
            <Alert variant="error">
              {error}
            </Alert>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={isLoading}
              disabled={!title.trim()}
            >
              {isEditing ? "Update Task" : "Create Task"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
