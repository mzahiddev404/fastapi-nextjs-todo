"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button, Input, Card, CardHeader, CardContent, Alert } from "@/components/ui";
import { useAuth } from "@/hooks/useAuth";

// Signup page component - handles user registration
export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const { signup } = useAuth();

  // Handle form submission for user registration
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      await signup(username, email, password);
      // Redirect to dashboard after successful signup
      router.push("/");
    } catch (err) {
      console.error("Signup error:", err);
      setError(err instanceof Error ? err.message : "Signup failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{" "}
            <Link
              href="/auth/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              sign in to your existing account
            </Link>
          </p>
        </div>
        
        <Card>
          <CardContent>
            <form className="space-y-6" onSubmit={handleSubmit}>
              <Input
                label="Username"
                type="text"
                autoComplete="username"
                required
                placeholder="Choose a username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              
              <Input
                label="Email address"
                type="email"
                autoComplete="email"
                required
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              
              <Input
                label="Password"
                type="password"
                autoComplete="new-password"
                required
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              {error && (
                <Alert variant="error">
                  {error}
                </Alert>
              )}

              <Button
                type="submit"
                isLoading={isLoading}
                className="w-full"
                size="lg"
              >
                {isLoading ? "Creating account..." : "Create account"}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
