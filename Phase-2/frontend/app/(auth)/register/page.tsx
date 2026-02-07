/**
 * Registration page
 *
 * Allows new users to create an account with email, name, and password.
 */
import { RegisterForm } from "@/components/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Create your account</h1>
          <p className="mt-2 text-sm text-gray-600">
            Join us and start managing your tasks efficiently
          </p>
        </div>

        {/* Registration form */}
        <div className="mt-8 bg-white py-8 px-6 shadow-lg rounded-lg sm:px-10">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}
