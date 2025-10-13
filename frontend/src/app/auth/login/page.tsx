"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button, Input, Alert } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";

// Professional login page with clean, modern design
export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const { login, startDemo } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      await login(email, password);
      router.push("/");
    } catch (err) {
      console.error("Login error:", err);
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemo = async () => {
    setIsLoading(true);
    setError("");

    try {
      await startDemo();
      router.push("/");
    } catch (err) {
      console.error("Demo error:", err);
      setError(err instanceof Error ? err.message : "Demo failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
          Welcome back
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Sign in to your TaskFlow account
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <div className="flex">
                <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div className="ml-3">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <div className="space-y-3">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </div>
                ) : (
                  "Sign in"
                )}
              </button>
              
              <button
                type="button"
                onClick={handleDemo}
                disabled={isLoading}
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Starting demo...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <span className="mr-2">🎯</span>
                    Try Demo
                  </div>
                )}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">New to TaskFlow?</span>
              </div>
            </div>

            <div className="mt-6">
              <Link
                href="/auth/signup"
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create an account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>

      {/* Enhanced Pattern Overlay with Texture */}
      <div className="absolute inset-0 opacity-[0.07]" style={{
        backgroundImage: `repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(120, 53, 15, 0.2) 10px, rgba(120, 53, 15, 0.2) 20px)`
      }}></div>
      
      {/* Additional Noise Texture for Paper Effect */}
      <div className="absolute inset-0 opacity-[0.03]" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='2' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
      }}></div>

      {/* Main Container */}
      <div className="relative z-10 max-w-md w-full">
        {/* Enhanced Vintage Header with Ornamental Border */}
        <div className="text-center mb-10">
          {/* Decorative Top Line with Better Contrast */}
          <div className="flex items-center justify-center mb-8">
            <div className="h-0.5 w-20 bg-gradient-to-r from-transparent via-amber-800 to-amber-600"></div>
            <div className="mx-4 relative">
              <div className="absolute inset-0 bg-amber-500/30 blur-lg"></div>
              <svg className="w-8 h-8 text-amber-800 relative z-10 drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" />
              </svg>
            </div>
            <div className="h-0.5 w-20 bg-gradient-to-l from-transparent via-amber-800 to-amber-600"></div>
          </div>

          {/* Enhanced Classic Typography with Better Shadows */}
          <div className="relative">
            <h1 className="text-6xl font-serif font-bold text-amber-950 mb-3 tracking-wide drop-shadow-xl">
              Welcome Back
            </h1>
            <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-48 h-1 bg-gradient-to-r from-transparent via-amber-600 to-transparent blur-sm"></div>
          </div>
          <p className="text-sm font-serif italic text-amber-800 tracking-[0.3em] uppercase mt-4 font-semibold">
            Est. 2025
          </p>
        </div>

        {/* Enhanced Classic Card with Deeper Vintage Border */}
        <div className="bg-gradient-to-br from-white via-amber-50/50 to-white backdrop-blur-sm shadow-[0_20px_60px_rgba(120,53,15,0.3)] rounded-xl border-4 border-amber-300 p-10 relative">
          {/* Multiple Decorative Borders for Depth */}
          <div className="absolute inset-4 border-2 border-amber-400/50 rounded-lg pointer-events-none"></div>
          <div className="absolute inset-6 border border-amber-300/30 rounded-md pointer-events-none"></div>
          
          {/* Corner Ornaments */}
          <div className="absolute top-2 left-2 w-6 h-6 border-t-2 border-l-2 border-amber-700 rounded-tl-lg"></div>
          <div className="absolute top-2 right-2 w-6 h-6 border-t-2 border-r-2 border-amber-700 rounded-tr-lg"></div>
          <div className="absolute bottom-2 left-2 w-6 h-6 border-b-2 border-l-2 border-amber-700 rounded-bl-lg"></div>
          <div className="absolute bottom-2 right-2 w-6 h-6 border-b-2 border-r-2 border-amber-700 rounded-br-lg"></div>
          
          <div className="relative">
            {/* Enhanced Subtitle with Shadow */}
            <div className="text-center mb-8">
              <h2 className="text-2xl font-serif font-bold text-amber-950 mb-2 drop-shadow-md tracking-wide">Sign In</h2>
              <div className="h-0.5 w-32 mx-auto bg-gradient-to-r from-transparent via-amber-700 to-transparent shadow-sm"></div>
            </div>

            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-2">
                <label className="block text-sm font-serif font-semibold text-amber-950 mb-2 tracking-wide">
                  Email Address
                </label>
                <input
                  type="email"
                  autoComplete="email"
                  required
                  placeholder="your.email@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-5 py-3.5 bg-gradient-to-br from-white to-amber-50/30 border-3 border-amber-400 rounded-lg focus:border-amber-700 focus:ring-4 focus:ring-amber-300/50 transition-all duration-300 font-serif text-amber-950 placeholder-amber-500 shadow-inner text-base"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-serif font-semibold text-amber-950 mb-2 tracking-wide">
                  Password
                </label>
                <input
                  type="password"
                  autoComplete="current-password"
                  required
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-5 py-3.5 bg-gradient-to-br from-white to-amber-50/30 border-3 border-amber-400 rounded-lg focus:border-amber-700 focus:ring-4 focus:ring-amber-300/50 transition-all duration-300 font-serif text-amber-950 placeholder-amber-500 shadow-inner text-base"
                />
              </div>

              {error && (
                <div className="bg-gradient-to-r from-red-100 to-red-50 border-3 border-red-400 text-red-900 px-5 py-4 rounded-lg text-sm font-serif shadow-lg">
                  <span className="font-semibold">⚠️ Error: </span>{error}
                </div>
              )}

              {/* Enhanced Classic Button with Better Depth */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-8 py-4 px-6 bg-gradient-to-br from-amber-700 via-amber-800 to-amber-900 text-white font-serif font-bold rounded-lg hover:from-amber-800 hover:via-amber-900 hover:to-amber-950 focus:outline-none focus:ring-4 focus:ring-amber-500/50 transform transition-all duration-300 hover:scale-[1.03] hover:shadow-2xl active:scale-[0.97] shadow-[0_10px_30px_rgba(120,53,15,0.4)] disabled:opacity-50 disabled:cursor-not-allowed text-lg tracking-wider border-2 border-amber-600"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </span>
                ) : "Sign In"}
              </button>

              {/* Enhanced Decorative Divider */}
              <div className="flex items-center my-8">
                <div className="flex-1 h-0.5 bg-gradient-to-r from-transparent via-amber-500 to-amber-400"></div>
                <span className="px-5 text-xs font-serif text-amber-800 italic font-semibold tracking-wider">or</span>
                <div className="flex-1 h-0.5 bg-gradient-to-l from-transparent via-amber-500 to-amber-400"></div>
              </div>

              {/* Enhanced Sign Up Link */}
              <div className="text-center">
                <p className="text-base font-serif text-amber-800 font-medium">
                  New here?{" "}
                  <Link
                    href="/auth/signup"
                    className="font-bold text-amber-950 hover:text-amber-700 underline decoration-2 decoration-amber-500 hover:decoration-amber-700 transition-all duration-300 underline-offset-4"
                  >
                    Create an account
                  </Link>
                </p>
              </div>
            </form>
          </div>
        </div>

        {/* Enhanced Footer Ornament */}
        <div className="text-center mt-10">
          <div className="flex items-center justify-center">
            <div className="h-0.5 w-16 bg-gradient-to-r from-transparent via-amber-600 to-amber-500"></div>
            <span className="mx-4 text-sm font-serif italic text-amber-800 tracking-wide font-medium">
              Crafted with care
            </span>
            <div className="h-0.5 w-16 bg-gradient-to-l from-transparent via-amber-600 to-amber-500"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
