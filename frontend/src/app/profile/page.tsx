"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button, Input, Alert, LoadingSpinner } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";

// User profile page
export default function ProfilePage() {
  const router = useRouter();
  const { user, isLoading: authLoading, error: authError, isAuthenticated } = useAuth();
  const { tasks, isLoading: tasksLoading } = useTasks();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: user?.username || "",
    email: user?.email || "",
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState("");

  // Redirect to login if not authenticated
  if (!authLoading && !isAuthenticated) {
    router.push("/auth/login");
    return null;
  }

  // Loading state
  if (authLoading || tasksLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading profile..." />
      </div>
    );
  }

  // Error state
  if (authError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full">
          <Alert variant="error" className="mb-4">
            <h2 className="text-lg font-semibold mb-2">Error Loading Profile</h2>
            <p className="text-sm">
              {authError.message || "Failed to load profile. Please try again."}
            </p>
          </Alert>
          <Button onClick={() => router.push("/")} className="w-full">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSaveError("");

    try {
      // TODO: Implement profile update API call
      // await updateProfile(formData);
      console.log("Profile update not implemented yet:", formData);
      setIsEditing(false);
    } catch (error) {
      setSaveError(error instanceof Error ? error.message : "Failed to update profile");
    } finally {
      setIsSaving(false);
    }
  };

  // Handle form changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  // Calculate task statistics
  const taskStats = {
    total: tasks.length,
    completed: tasks.filter(task => task.status === "complete").length,
    pending: tasks.filter(task => task.status === "incomplete").length,
    overdue: tasks.filter(task => 
      task.deadline && 
      new Date(task.deadline) < new Date() && 
      task.status !== "complete"
    ).length,
  };

  const completionRate = taskStats.total > 0 
    ? Math.round((taskStats.completed / taskStats.total) * 100) 
    : 0;

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
              <h1 className="text-xl font-semibold text-gray-900">Profile</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="space-y-6">
            {/* Profile Information */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-medium text-gray-900">Profile Information</h2>
                  <Button
                    onClick={() => setIsEditing(!isEditing)}
                    variant="secondary"
                    size="sm"
                  >
                    {isEditing ? "Cancel" : "Edit"}
                  </Button>
                </div>
              </div>

              <div className="px-6 py-4">
                {isEditing ? (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    {saveError && (
                      <Alert variant="error">
                        {saveError}
                      </Alert>
                    )}
                    
                    <div>
                      <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                        Username
                      </label>
                      <Input
                        id="username"
                        name="username"
                        type="text"
                        value={formData.username}
                        onChange={handleChange}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                      </label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                      />
                    </div>

                    <div className="flex items-center space-x-3">
                      <Button
                        type="submit"
                        
                        disabled={isSaving}
                      >
                        {isSaving ? "Saving..." : "Save Changes"}
                      </Button>
                      <Button
                        type="button"
                        variant="secondary"
                        onClick={() => {
                          setIsEditing(false);
                          setFormData({
                            username: user?.username || "",
                            email: user?.email || "",
                          });
                          setSaveError("");
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </form>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Username
                      </label>
                      <p className="text-sm text-gray-900">{user?.username || "N/A"}</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                      </label>
                      <p className="text-sm text-gray-900">{user?.email || "N/A"}</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Member Since
                      </label>
                      <p className="text-sm text-gray-900">
                        {user?.created_at 
                          ? new Date(user.created_at).toLocaleDateString("en-US", {
                              year: "numeric",
                              month: "long",
                              day: "numeric",
                            })
                          : "N/A"
                        }
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Task Statistics */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Task Statistics</h2>
              </div>

              <div className="px-6 py-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{taskStats.total}</div>
                    <div className="text-sm text-gray-500">Total Tasks</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{taskStats.completed}</div>
                    <div className="text-sm text-gray-500">Completed</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">{taskStats.pending}</div>
                    <div className="text-sm text-gray-500">Pending</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">{taskStats.overdue}</div>
                    <div className="text-sm text-gray-500">Overdue</div>
                  </div>
                </div>

                <div className="mt-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Completion Rate</span>
                    <span className="text-sm text-gray-500">{completionRate}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${completionRate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
              </div>

              <div className="px-6 py-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Button
                    onClick={() => router.push("/")}
                    
                    className="w-full"
                  >
                    View All Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/pending")}
                    variant="secondary"
                    className="w-full"
                  >
                    View Pending Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/completed")}
                    variant="secondary"
                    className="w-full"
                  >
                    View Completed Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/")}
                    variant="secondary"
                    className="w-full"
                  >
                    Create New Task
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
