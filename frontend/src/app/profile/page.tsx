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
    <div className="min-h-screen relative overflow-hidden">
      {/* Floating particles background */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-10 w-32 h-32 bg-yellow-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '3s' }}></div>
        <div className="absolute top-1/3 right-20 w-40 h-40 bg-pink-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-36 h-36 bg-cyan-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '5s', animationDelay: '2s' }}></div>
        <div className="absolute bottom-1/4 right-1/4 w-28 h-28 bg-purple-400/30 rounded-full blur-2xl animate-bounce" style={{ animationDuration: '6s', animationDelay: '0.5s' }}></div>
      </div>

      {/* Header */}
      <header className="bg-white/95 backdrop-blur-xl border-b-2 border-indigo-200/50 shadow-[0_10px_40px_-10px_rgba(79,70,229,0.3)] relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-50/80 via-purple-50/60 to-pink-50/80 opacity-70"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1500"></div>
        
        <div className="max-w-7xl mx-auto py-4 sm:py-5 px-3 sm:px-6 lg:px-8 relative z-10">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2 sm:gap-3">
              <Button
                variant="secondary"
                onClick={() => router.push("/")}
                className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold px-2.5 sm:px-4"
              >
                <svg className="w-4 h-4 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span className="hidden sm:inline">Back</span>
              </Button>
              <h1 className="text-lg sm:text-2xl md:text-3xl font-extrabold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">My Profile</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-5xl mx-auto py-4 sm:py-6 md:py-8 px-3 sm:px-6 lg:px-8">
        <div className="space-y-4 sm:space-y-6">
            {/* Profile Information */}
            <div className="transform hover:scale-[1.01] transition-transform duration-300">
              <div className="bg-white/95 backdrop-blur-xl shadow-[0_25px_80px_-15px_rgba(79,70,229,0.5)] border-2 border-indigo-200/50 rounded-2xl overflow-hidden relative group hover:border-indigo-300 hover:shadow-[0_30px_90px_-15px_rgba(79,70,229,0.6)] transition-all duration-500">
                {/* Animated gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/60 via-purple-100/40 to-pink-100/60 opacity-60 pointer-events-none"></div>
                {/* Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
                
                <div className="border-b-2 border-indigo-200/50 bg-gradient-to-r from-indigo-100/80 via-purple-100/60 to-pink-100/80 p-4 sm:p-6 relative z-10">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                    <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                      <svg className="w-5 h-5 sm:w-6 sm:h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Profile Information
                    </h2>
                    <Button
                      onClick={() => setIsEditing(!isEditing)}
                      variant="secondary"
                      size="sm"
                      className="w-full sm:w-auto bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                    >
                      {isEditing ? "Cancel" : "Edit"}
                    </Button>
                  </div>
                </div>

                <div className="p-4 sm:p-6 relative z-10">
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
            </div>

            {/* Change Password */}
            <div className="transform hover:scale-[1.01] transition-transform duration-300">
              <div className="bg-white/95 backdrop-blur-xl shadow-[0_25px_80px_-15px_rgba(168,85,247,0.5)] border-2 border-purple-200/50 rounded-2xl overflow-hidden relative group hover:border-purple-300 hover:shadow-[0_30px_90px_-15px_rgba(168,85,247,0.6)] transition-all duration-500">
                {/* Animated gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-purple-100/60 via-pink-100/40 to-rose-100/60 opacity-60 pointer-events-none"></div>
                {/* Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
                
                <div className="border-b-2 border-purple-200/50 bg-gradient-to-r from-purple-100/80 via-pink-100/60 to-rose-100/80 p-4 sm:p-6 relative z-10">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                    <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                      <svg className="w-5 h-5 sm:w-6 sm:h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                        className="w-full sm:w-auto bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                      >
                        Change Password
                      </Button>
                    )}
                  </div>
                </div>

                <div className="p-4 sm:p-6 relative z-10">
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
            </div>

            {/* Task Statistics */}
            <div className="transform hover:scale-[1.01] transition-transform duration-300">
              <div className="bg-white/95 backdrop-blur-xl shadow-[0_25px_80px_-15px_rgba(59,130,246,0.5)] border-2 border-blue-200/50 rounded-2xl overflow-hidden relative group hover:border-blue-300 hover:shadow-[0_30px_90px_-15px_rgba(59,130,246,0.6)] transition-all duration-500">
                {/* Animated gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-100/60 via-cyan-100/40 to-indigo-100/60 opacity-60 pointer-events-none"></div>
                {/* Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
                
                <div className="border-b-2 border-blue-200/50 bg-gradient-to-r from-blue-100/80 via-cyan-100/60 to-indigo-100/80 p-4 sm:p-6 relative z-10">
                  <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Task Statistics
                  </h2>
                </div>

                <div className="p-4 sm:p-6 relative z-10">
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
            </div>

            {/* Quick Actions */}
            <div className="transform hover:scale-[1.01] transition-transform duration-300">
              <div className="bg-white/95 backdrop-blur-xl shadow-[0_25px_80px_-15px_rgba(16,185,129,0.5)] border-2 border-emerald-200/50 rounded-2xl overflow-hidden relative group hover:border-emerald-300 hover:shadow-[0_30px_90px_-15px_rgba(16,185,129,0.6)] transition-all duration-500">
                {/* Animated gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-100/60 via-teal-100/40 to-cyan-100/60 opacity-60 pointer-events-none"></div>
                {/* Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
                
                <div className="border-b-2 border-emerald-200/50 bg-gradient-to-r from-emerald-100/80 via-teal-100/60 to-cyan-100/80 p-4 sm:p-6 relative z-10">
                  <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Quick Actions
                  </h2>
                </div>

                <div className="p-4 sm:p-6 relative z-10">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                  <Button
                    onClick={() => router.push("/")}
                    className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    View All Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/incomplete")}
                    variant="secondary"
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    View Pending Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/tasks/status/complete")}
                    variant="secondary"
                    className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    View Completed Tasks
                  </Button>
                  
                  <Button
                    onClick={() => router.push("/")}
                    variant="secondary"
                    className="w-full bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Create New Task
                  </Button>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
