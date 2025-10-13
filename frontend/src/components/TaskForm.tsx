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
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState<"low" | "medium" | "high">(task?.priority || "medium");
  const [dueDate, setDueDate] = useState(task?.due_date || "");
  const [selectedLabels, setSelectedLabels] = useState<string[]>(task?.label_ids || []);
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
      const taskData: TaskCreate | TaskUpdate = {
        title,
        description: description || undefined,
        priority,
        due_date: dueDate || undefined,
        label_ids: selectedLabels.length > 0 ? selectedLabels : undefined,
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

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <h3 id="task-form-title" className="text-lg font-medium text-gray-900">
          {isEditing ? "Edit Task" : "Create New Task"}
        </h3>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title"
            required
          />

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
                Due Date
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
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
