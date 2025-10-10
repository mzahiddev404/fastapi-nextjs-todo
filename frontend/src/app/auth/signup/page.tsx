"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

// Nostalgic and classic signup page with enhanced vintage aesthetics
export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const { signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      await signup(username, email, password);
      router.push("/");
    } catch (err) {
      console.error("Signup error:", err);
      setError(err instanceof Error ? err.message : "Signup failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Rich Vintage Background with Deep Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-100 via-orange-100 to-yellow-100"></div>
      <div className="absolute inset-0 bg-gradient-to-tr from-amber-900/10 via-transparent to-orange-900/10"></div>
      
      {/* Enhanced Decorative Corners - Top Left */}
      <div className="absolute top-0 left-0 w-40 h-40 opacity-30">
        <div className="absolute top-6 left-6 w-28 h-28 border-t-[6px] border-l-[6px] border-amber-900 rounded-tl-[2rem]"></div>
        <div className="absolute top-8 left-8 w-24 h-24 border-t-2 border-l-2 border-orange-700 rounded-tl-3xl"></div>
      </div>
      
      {/* Enhanced Decorative Corners - Bottom Right */}
      <div className="absolute bottom-0 right-0 w-40 h-40 opacity-30">
        <div className="absolute bottom-6 right-6 w-28 h-28 border-b-[6px] border-r-[6px] border-amber-900 rounded-br-[2rem]"></div>
        <div className="absolute bottom-8 right-8 w-24 h-24 border-b-2 border-r-2 border-orange-700 rounded-br-3xl"></div>
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
        {/* Enhanced Vintage Header */}
        <div className="text-center mb-10">
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

          <div className="relative">
            <h1 className="text-6xl font-serif font-bold text-amber-950 mb-3 tracking-wide drop-shadow-xl">
              Join Us
            </h1>
            <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-48 h-1 bg-gradient-to-r from-transparent via-amber-600 to-transparent blur-sm"></div>
          </div>
          <p className="text-sm font-serif italic text-amber-800 tracking-[0.3em] uppercase mt-4 font-semibold">
            Begin Your Journey
          </p>
        </div>

        {/* Enhanced Card */}
        <div className="bg-gradient-to-br from-white via-amber-50/50 to-white backdrop-blur-sm shadow-[0_20px_60px_rgba(120,53,15,0.3)] rounded-xl border-4 border-amber-300 p-10 relative">
          {/* Multiple Decorative Borders */}
          <div className="absolute inset-4 border-2 border-amber-400/50 rounded-lg pointer-events-none"></div>
          <div className="absolute inset-6 border border-amber-300/30 rounded-md pointer-events-none"></div>
          
          {/* Corner Ornaments */}
          <div className="absolute top-2 left-2 w-6 h-6 border-t-2 border-l-2 border-amber-700 rounded-tl-lg"></div>
          <div className="absolute top-2 right-2 w-6 h-6 border-t-2 border-r-2 border-amber-700 rounded-tr-lg"></div>
          <div className="absolute bottom-2 left-2 w-6 h-6 border-b-2 border-l-2 border-amber-700 rounded-bl-lg"></div>
          <div className="absolute bottom-2 right-2 w-6 h-6 border-b-2 border-r-2 border-amber-700 rounded-br-lg"></div>
          
          <div className="relative">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-serif font-bold text-amber-950 mb-2 drop-shadow-md tracking-wide">Create Account</h2>
              <div className="h-0.5 w-32 mx-auto bg-gradient-to-r from-transparent via-amber-700 to-transparent shadow-sm"></div>
            </div>

            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-2">
                <label className="block text-sm font-serif font-semibold text-amber-950 mb-2 tracking-wide">
                  Username
                </label>
                <input
                  type="text"
                  autoComplete="username"
                  required
                  placeholder="Choose a username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-5 py-3.5 bg-gradient-to-br from-white to-amber-50/30 border-3 border-amber-400 rounded-lg focus:border-amber-700 focus:ring-4 focus:ring-amber-300/50 transition-all duration-300 font-serif text-amber-950 placeholder-amber-500 shadow-inner text-base"
                />
              </div>

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
                  autoComplete="new-password"
                  required
                  placeholder="Create a password"
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
                    Creating account...
                  </span>
                ) : "Create Account"}
              </button>

              <div className="flex items-center my-8">
                <div className="flex-1 h-0.5 bg-gradient-to-r from-transparent via-amber-500 to-amber-400"></div>
                <span className="px-5 text-xs font-serif text-amber-800 italic font-semibold tracking-wider">or</span>
                <div className="flex-1 h-0.5 bg-gradient-to-l from-transparent via-amber-500 to-amber-400"></div>
              </div>

              <div className="text-center">
                <p className="text-base font-serif text-amber-800 font-medium">
                  Already have an account?{" "}
                  <Link
                    href="/auth/login"
                    className="font-bold text-amber-950 hover:text-amber-700 underline decoration-2 decoration-amber-500 hover:decoration-amber-700 transition-all duration-300 underline-offset-4"
                  >
                    Sign in
                  </Link>
                </p>
              </div>
            </form>
          </div>
        </div>

        {/* Footer */}
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
