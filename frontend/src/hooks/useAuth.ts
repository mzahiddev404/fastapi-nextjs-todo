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
      const response = await api.post("/api/v1/auth/login", { email, password });
      localStorage.setItem("todo_token", response.access_token);
      mutate(); // Revalidate user data
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Signup function
  const signup = async (username: string, email: string, password: string) => {
    try {
      const response = await api.post("/api/v1/auth/signup", { username, email, password });
      localStorage.setItem("todo_token", response.access_token);
      mutate(); // Revalidate user data
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem("todo_token");
    mutate(null, false); // Clear user data without revalidation
  };

  return {
    user,
    isLoading,
    error,
    isAuthenticated: !!user && !error,
    login,
    signup,
    logout,
    mutate,
  };
}
