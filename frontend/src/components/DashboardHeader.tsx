"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui";
import { User } from "@/types";

interface DashboardHeaderProps {
  user: User;
  onLogout: () => void;
}

export function DashboardHeader({ user, onLogout }: DashboardHeaderProps) {
  const router = useRouter();

  return (
    <header id="navigation" className="bg-white border-b border-gray-200 shadow-sm" role="banner">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">TaskFlow</h1>
                <p className="text-sm text-gray-500">Productivity Management</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden sm:block text-right">
              <p className="text-sm font-medium text-gray-900">
                {user?.name || user?.email || "User"}
              </p>
              <p className="text-xs text-gray-500">Welcome back</p>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => router.push("/profile")}
                variant="ghost"
                size="sm"
                className="text-gray-600 hover:text-gray-900"
                aria-label="View your profile"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Profile
              </Button>
              <Button
                onClick={onLogout}
                variant="ghost"
                size="sm"
                className="text-gray-600 hover:text-red-600"
                aria-label="Logout from your account"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
