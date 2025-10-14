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
    <header id="navigation" className="bg-white/95 backdrop-blur-xl border-b-2 border-indigo-200/50 shadow-[0_10px_40px_-10px_rgba(79,70,229,0.3)] relative overflow-hidden group" role="banner">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-50/80 via-purple-50/60 to-pink-50/80 opacity-70"></div>
      {/* Shine effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1500"></div>
      
      <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 relative z-10">
        <div className="flex flex-col lg:flex-row justify-between items-stretch lg:items-center py-3 sm:py-4 lg:py-5 gap-3 lg:gap-4">
          {/* Logo and Title Section */}
          <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-shrink overflow-hidden">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-xl sm:rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-300/50 animate-pulse flex-shrink-0" style={{ animationDuration: '3s' }}>
              <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div className="min-w-0 flex-1 overflow-hidden">
              <h1 className="text-sm xs:text-base sm:text-xl md:text-2xl lg:text-3xl font-extrabold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent leading-tight">
                <span className="hidden md:inline">Remember The Milk... And Everything Else</span>
                <span className="hidden sm:inline md:hidden break-words">Remember The Milk... And Everything Else</span>
                <span className="inline sm:hidden break-words">Remember The Milk<br />...And Everything Else</span>
              </h1>
              <p className="text-[10px] xs:text-xs sm:text-sm font-semibold text-indigo-600/80 flex items-center gap-1 sm:gap-1.5 truncate mt-0.5">
                <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-emerald-500 rounded-full animate-pulse flex-shrink-0"></span>
                <span className="truncate">Productivity Management</span>
              </p>
            </div>
          </div>
          
          {/* User Info and Actions Section */}
          <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
            {/* User avatar and info - only show on larger screens */}
            <div className="hidden xl:flex items-center gap-2 sm:gap-3 bg-white/80 backdrop-blur-sm px-3 py-1.5 sm:px-4 sm:py-2 rounded-xl shadow-lg border border-indigo-100 flex-shrink-0">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg text-sm sm:text-base flex-shrink-0">
                {(user?.name || user?.email || "U").charAt(0).toUpperCase()}
              </div>
              <div className="text-right overflow-hidden">
                <p className="text-xs sm:text-sm font-bold text-gray-900 truncate max-w-[120px]">
                  {user?.name || user?.email || "User"}
                </p>
                <p className="text-[10px] sm:text-xs font-medium text-indigo-600 whitespace-nowrap">Welcome back! 👋</p>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex items-center gap-1.5 sm:gap-2">
              <Button
                onClick={() => router.push("/profile")}
                variant="ghost"
                size="sm"
                className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold px-2.5 sm:px-3 py-1.5 sm:py-2 text-xs sm:text-sm flex items-center gap-1.5"
                aria-label="View your profile"
              >
                <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-white font-bold text-xs flex-shrink-0">
                  {(user?.name || user?.email || "U").charAt(0).toUpperCase()}
                </div>
                <span className="hidden sm:inline truncate max-w-[100px]">{user?.name || user?.email?.split('@')[0] || "Profile"}</span>
                <span className="inline sm:hidden">Profile</span>
              </Button>
              <Button
                onClick={onLogout}
                variant="ghost"
                size="sm"
                className="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 border-0 font-semibold px-2.5 sm:px-3 py-1.5 sm:py-2 text-xs sm:text-sm whitespace-nowrap"
                aria-label="Logout from your account"
              >
                <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 sm:mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="hidden sm:inline">Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
