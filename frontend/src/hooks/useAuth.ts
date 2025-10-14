// Custom hook for authentication state management using SWR
import { useState, useEffect } from "react";
import useSWR from "swr";
import { User } from "@/types";
import { api } from "@/lib/apiClient";

// Fetcher function for SWR
const fetcher = (url: string) => api.get<User>(url);

export function useAuth() {
  const [isClient, setIsClient] = useState(false);
  
  // Ensure we're on the client side before checking localStorage
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Get token from localStorage (only on client side)
  const getToken = () => {
    if (!isClient) return null;
    return localStorage.getItem("todo_token");
  };

  const token = getToken();
  
  // Use SWR to fetch user data
  const { data: user, error, mutate, isLoading } = useSWR(
    token ? "/api/v1/auth/me" : null,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      dedupingInterval: 60000, // Cache for 1 minute
      shouldRetryOnError: false, // Don't retry on auth errors
      errorRetryCount: 0, // Don't retry at all
    }
  );

  // Login function
  const login = async (email: string, password: string) => {
    try {
      const response = await api.post("/api/v1/auth/login/json", { email, password });
      // Token is automatically stored by the API client
      mutate(); // Revalidate user data
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Signup function
  const signup = async (username: string, email: string, password: string) => {
    try {
      const response = await api.post("/api/v1/auth/signup", { name: username, email, password });
      // Token is automatically stored by the API client
      mutate(); // Revalidate user data
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Demo function
  const startDemo = async () => {
    try {
      const response = await api.post("/api/v1/auth/demo", {});
      // Token is automatically stored by the API client
      mutate(); // Revalidate user data
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Update profile function
  const updateProfile = async (name?: string, email?: string) => {
    try {
      const response = await api.put("/api/v1/auth/profile", { name, email });
      mutate(); // Revalidate user data to reflect changes
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Change password function
  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      const response = await api.put("/api/v1/auth/password", { 
        current_password: currentPassword, 
        new_password: newPassword 
      });
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Logout function
  const logout = () => {
    // Remove token from localStorage
    if (typeof window !== "undefined") {
      localStorage.removeItem("todo_token");
    }
    mutate(undefined, false); // Clear user data without revalidation
  };

  return {
    user,
    isLoading,
    error,
    isAuthenticated: !!user && !error,
    isDemo: user?.is_demo || false,
    login,
    signup,
    startDemo,
    logout,
    updateProfile,
    changePassword,
    mutate,
  };
}
