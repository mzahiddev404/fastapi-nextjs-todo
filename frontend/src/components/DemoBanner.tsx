"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";

interface DemoBannerProps {
  onUpgrade?: () => void;
}

export function DemoBanner({ onUpgrade }: DemoBannerProps) {
  const { isDemo, logout } = useAuth();
  const [isCleaning, setIsCleaning] = useState(false);
  const router = useRouter();

  if (!isDemo) return null;

  const handleCleanup = async () => {
    setIsCleaning(true);
    try {
      await fetch("/api/v1/auth/demo/cleanup", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("todo_token")}`,
        },
      });
      // Refresh the page to show clean demo data
      window.location.reload();
    } catch (error) {
      console.error("Failed to cleanup demo data:", error);
    } finally {
      setIsCleaning(false);
    }
  };

  const handleUpgrade = () => {
    logout();
    router.push("/auth/signup");
  };

  return (
    <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-3">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold">🎯</span>
              </div>
            </div>
            <div>
              <p className="text-sm font-medium">
                You're in <strong>Demo Mode</strong> - Try all features with sample data!
              </p>
              <p className="text-xs text-blue-100">
                This is a preview account with sample tasks and labels
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              onClick={handleCleanup}
              variant="secondary"
              size="sm"
              disabled={isCleaning}
              className="bg-white bg-opacity-20 text-white hover:bg-opacity-30 border-white border-opacity-30"
            >
              {isCleaning ? "Cleaning..." : "Reset Demo"}
            </Button>
            
            <Button
              onClick={handleUpgrade}
              variant="secondary"
              size="sm"
              className="bg-white text-blue-600 hover:bg-gray-50 font-medium"
            >
              Create Account
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

