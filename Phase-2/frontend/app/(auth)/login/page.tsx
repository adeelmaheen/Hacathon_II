/**
 * Login page
 *
 * Allows existing users to log in with email and password.
 */
import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Welcome back</h1>
          <p className="mt-2 text-sm text-gray-600">
            Log in to access your tasks and stay organized
          </p>
        </div>

        {/* Login form */}
        <div className="mt-8 bg-white py-8 px-6 shadow-lg rounded-lg sm:px-10">
          <LoginForm />
        </div>
      </div>
    </div>
  );
}
