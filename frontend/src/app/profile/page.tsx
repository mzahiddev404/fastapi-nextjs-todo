"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { Button, Input, Alert, LoadingSpinner } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";

// User profile page
export default function ProfilePage() {
  const router = useRouter();
  const { user, isLoading: authLoading, error: authError, isAuthenticated, updateProfile, changePassword } = useAuth();
  const { tasks, isLoading: tasksLoading } = useTasks();
  const [isEditing, setIsEditing] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || "",
    email: user?.email || "",
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isMounted, setIsMounted] = useState(false);
  const [hasToken, setHasToken] = useState(false);

  // Check if component is mounted and if token exists (client-side only)
  useEffect(() => {
    setIsMounted(true);
    if (typeof window !== 'undefined') {
      setHasToken(!!localStorage.getItem('todo_token'));
    }
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (isMounted && !authLoading && !isAuthenticated && !hasToken) {
      router.push("/auth/login");
    }
  }, [isMounted, authLoading, isAuthenticated, hasToken, router]);

  // Show loading while checking authentication or during SSR
  if (!isMounted || authLoading || (hasToken && !user && !authError)) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading profile..." />
      </div>
    );
  }

  // Don't render anything while redirecting
  if (!isAuthenticated && !hasToken) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Redirecting..." />
      </div>
    );
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
    
    // Build list of changes
    const changes = [];
    if (formData.name !== user?.name) {
      changes.push(`name to "${formData.name || 'Not set'}"`);
    }
    if (formData.email !== user?.email) {
      changes.push(`email to "${formData.email}"`);
    }
    
    // If no changes, don't proceed
    if (changes.length === 0) {
      setSaveError("No changes detected");
      return;
    }
    
    // Ask for confirmation
    const changeText = changes.length === 1 
      ? `Change ${changes[0]}`
      : `Change ${changes.join(" and ")}`;
    
    if (!window.confirm(`${changeText}?\n\nThis will update your profile information.`)) {
      return;
    }
    
    setIsSaving(true);
    setSaveError("");
    setSuccessMessage("");

    try {
      await updateProfile(formData.name, formData.email);
      setSuccessMessage("Profile updated successfully!");
      setIsEditing(false);
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (error) {
      let errorMessage = "Failed to update profile";
      
      if (error instanceof Error) {
        // Handle specific error messages
        if (error.message.includes("Failed to fetch")) {
          errorMessage = "Cannot connect to server. Please check your internet connection.";
        } else if (error.message.includes("Email already registered")) {
          errorMessage = "This email is already in use by another account.";
        } else {
          errorMessage = error.message;
        }
      }
      
      setSaveError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  // Handle password change
  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaveError("");
    setSuccessMessage("");

    // Validate passwords match
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setSaveError("New passwords do not match");
      return;
    }

    // Validate password length
    if (passwordData.newPassword.length < 8) {
      setSaveError("Password must be at least 8 characters");
      return;
    }
    
    // Ask for confirmation
    if (!window.confirm("Change your password?\n\nYou will need to use the new password for future logins.")) {
      return;
    }

    setIsSaving(true);

    try {
      await changePassword(passwordData.currentPassword, passwordData.newPassword);
      setSuccessMessage("Password updated successfully!");
      setIsChangingPassword(false);
      setPasswordData({
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      });
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (error) {
      let errorMessage = "Failed to update password";
      
      if (error instanceof Error) {
        // Handle specific error messages
        if (error.message.includes("Failed to fetch")) {
          errorMessage = "Cannot connect to server. Please check your internet connection.";
        } else if (error.message.includes("Current password is incorrect")) {
          errorMessage = "Current password is incorrect. Please try again.";
        } else {
          errorMessage = error.message;
        }
      }
      
      setSaveError(errorMessage);
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

  // Handle password form changes
  const handlePasswordDataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-indigo-50/30 to-purple-50/30">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-sm shadow-lg border-b-2 border-indigo-100">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="secondary"
                onClick={() => router.push("/")}
                className="flex items-center space-x-2 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white border-0"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back to Dashboard</span>
              </Button>
              <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">My Profile</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="space-y-6">
            {/* Profile Information */}
            <div className="bg-white/90 backdrop-blur-sm shadow-xl rounded-2xl border-2 border-indigo-100 overflow-hidden">
              <div className="px-6 py-4 border-b-2 border-indigo-100 bg-gradient-to-r from-indigo-50 to-purple-50">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    Profile Information
                  </h2>
                  <Button
                    onClick={() => setIsEditing(!isEditing)}
                    variant="secondary"
                    size="sm"
                    className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white border-0"
                  >
                    {isEditing ? "Cancel" : "Edit"}
                  </Button>
                </div>
              </div>

              <div className="px-6 py-4">
                {successMessage && (
                  <Alert variant="success" className="mb-4">
                    {successMessage}
                  </Alert>
                )}
                
                {isEditing ? (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    {saveError && (
                      <Alert variant="error">
                        {saveError}
                      </Alert>
                    )}
                    
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                        Name
                      </label>
                      <Input
                        id="name"
                        name="name"
                        type="text"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Your name"
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
                            name: user?.name || "",
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
                        Name
                      </label>
                      <p className="text-sm text-gray-900">{user?.name || "Not set"}</p>
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

            {/* Change Password */}
            <div className="bg-white/90 backdrop-blur-sm shadow-xl rounded-2xl border-2 border-purple-100 overflow-hidden">
              <div className="px-6 py-4 border-b-2 border-purple-100 bg-gradient-to-r from-purple-50 to-pink-50">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    Change Password
                  </h2>
                  {!isChangingPassword && (
                    <Button
                      onClick={() => {
                        setIsChangingPassword(true);
                        setSaveError("");
                        setSuccessMessage("");
                      }}
                      variant="secondary"
                      size="sm"
                      className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white border-0"
                    >
                      Change Password
                    </Button>
                  )}
                </div>
              </div>

              <div className="px-6 py-4">
                {isChangingPassword ? (
                  <form onSubmit={handlePasswordChange} className="space-y-4">
                    <div>
                      <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700 mb-1">
                        Current Password
                      </label>
                      <Input
                        id="currentPassword"
                        name="currentPassword"
                        type="password"
                        value={passwordData.currentPassword}
                        onChange={handlePasswordDataChange}
                        placeholder="Enter current password"
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                        New Password
                      </label>
                      <Input
                        id="newPassword"
                        name="newPassword"
                        type="password"
                        value={passwordData.newPassword}
                        onChange={handlePasswordDataChange}
                        placeholder="Enter new password (min 8 characters)"
                        required
                        minLength={8}
                      />
                    </div>

                    <div>
                      <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                        Confirm New Password
                      </label>
                      <Input
                        id="confirmPassword"
                        name="confirmPassword"
                        type="password"
                        value={passwordData.confirmPassword}
                        onChange={handlePasswordDataChange}
                        placeholder="Re-enter new password"
                        required
                        minLength={8}
                      />
                    </div>

                    <div className="flex items-center space-x-3">
                      <Button
                        type="submit"
                        disabled={isSaving}
                      >
                        {isSaving ? "Updating..." : "Update Password"}
                      </Button>
                      <Button
                        type="button"
                        variant="secondary"
                        onClick={() => {
                          setIsChangingPassword(false);
                          setPasswordData({
                            currentPassword: "",
                            newPassword: "",
                            confirmPassword: "",
                          });
                          setSaveError("");
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </form>
                ) : (
                  <p className="text-sm text-gray-600">
                    Click "Change Password" to update your password securely.
                  </p>
                )}
              </div>
            </div>

            {/* Task Statistics */}
            <div className="bg-white/90 backdrop-blur-sm shadow-xl rounded-2xl border-2 border-pink-100 overflow-hidden">
              <div className="px-6 py-4 border-b-2 border-pink-100 bg-gradient-to-r from-pink-50 to-purple-50">
                <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                  <svg className="w-5 h-5 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Task Statistics
                </h2>
              </div>

              <div className="px-6 py-4">
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="text-center bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border-2 border-blue-100">
                    <div className="text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">{taskStats.total}</div>
                    <div className="text-sm font-semibold text-gray-700 mt-1">Total Tasks</div>
                  </div>
                  
                  <div className="text-center bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 border-2 border-green-100">
                    <div className="text-3xl font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">{taskStats.completed}</div>
                    <div className="text-sm font-semibold text-gray-700 mt-1">Completed</div>
                  </div>
                  
                  <div className="text-center bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl p-4 border-2 border-yellow-100">
                    <div className="text-3xl font-extrabold bg-gradient-to-r from-yellow-600 to-amber-600 bg-clip-text text-transparent">{taskStats.pending}</div>
                    <div className="text-sm font-semibold text-gray-700 mt-1">Pending</div>
                  </div>
                  
                  <div className="text-center bg-gradient-to-br from-red-50 to-pink-50 rounded-xl p-4 border-2 border-red-100">
                    <div className="text-3xl font-extrabold bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent">{taskStats.overdue}</div>
                    <div className="text-sm font-semibold text-gray-700 mt-1">Overdue</div>
                  </div>
                </div>

                <div className="mt-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-bold text-gray-900">Completion Rate</span>
                    <span className="text-sm font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">{completionRate}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner">
                    <div
                      className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${completionRate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white/90 backdrop-blur-sm shadow-xl rounded-2xl border-2 border-indigo-100 overflow-hidden">
              <div className="px-6 py-4 border-b-2 border-indigo-100 bg-gradient-to-r from-indigo-50 to-cyan-50">
                <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                  <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Quick Actions
                </h2>
              </div>

              <div className="px-6 py-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <Button
                    onClick={() => router.push("/")}
                    className="w-full bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 font-semibold h-12"
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    View All Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/pending")}
                    className="w-full bg-gradient-to-r from-yellow-500 to-amber-500 hover:from-yellow-600 hover:to-amber-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 font-semibold h-12"
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    View Pending
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/completed")}
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 font-semibold h-12"
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    View Completed
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/")}
                    className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 font-semibold h-12"
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
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
