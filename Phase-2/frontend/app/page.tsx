/**
 * Landing page - redirects based on auth state
 */
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (user) {
        // Redirect authenticated users to dashboard
        router.push("/dashboard");
      } else {
        // Redirect unauthenticated users to login
        router.push("/login");
      }
    }
  }, [user, loading, router]);

  // Show loading state while checking auth
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-lg text-gray-600">Loading...</div>
    </main>
  );
}
