"use client";

import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { getMe, login } from "@/services/auth";
import { useRouter } from "next/navigation";
import GoogleButton from "@/components/auth/GoogleButton";
import Link from "next/link";
import { toast } from "sonner";

// Validation Schema using Yup
const loginSchema = Yup.object().shape({
  email: Yup.string()
    .email("Invalid email address")
    .required("Email is required"),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),
});

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  // Formik hook initialization
  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema: loginSchema,
    onSubmit: async (values) => {
      try {
        setLoading(true);
        await login(values.email, values.password);
        toast.success("Login successful");
        setTimeout(() => {
          router.replace("/home");
        }, 3000);
      } catch (error: any) {
        toast.error(error?.response?.data?.detail ?? "Login failed");
      } finally {
        setLoading(false);
      }
    },
  });

  const callme = async () => {
    const result = await getMe();
    toast.success("called");
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#F9FBF9] px-4 py-12 sm:px-6 lg:px-8">
      {/* Top Application Logo Header */}
      <div
        onClick={() => {
          router.push("/");
        }}
        className="cursor-pointer transition-all duration-300 ease-in-out text-shadow-[0px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 p-1 rounded-md mb-3 flex items-center gap-2 font-bold text-neutral-900 text-lg"
      >
        FoodSnapAI
      </div>

      <div className="w-full max-w-md space-y-6 rounded-[2.5rem] bg-white p-10 shadow-sm border border-neutral-100/60">
        {/* Header */}
        <div className="text-left space-y-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-neutral-950">
            Welcome back
          </h2>
          <p className="text-sm text-neutral-500 font-medium">
            Log in to continue analyzing your meals.
          </p>
        </div>

        <div className="space-y-6">
          {/* Form */}
          <form className="space-y-5" onSubmit={formik.handleSubmit}>
            <div className="space-y-4">
              {/* Email Field */}
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-semibold text-neutral-800"
                >
                  Email
                </label>
                <div className="mt-1.5">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className={`block w-full rounded-xl border bg-neutral-50/50 px-4 py-3 text-neutral-900 placeholder-neutral-400 shadow-sm transition-all focus:outline-none focus:ring-1 ${
                      formik.touched.email && formik.errors.email
                        ? "border-red-400 focus:border-red-400 focus:ring-red-400"
                        : "border-neutral-200 focus:border-green-500 focus:ring-green-500"
                    }`}
                    placeholder="you@example.com"
                  />
                </div>
                {formik.touched.email && formik.errors.email && (
                  <p className="mt-1 text-xs text-red-500 font-medium">
                    {formik.errors.email}
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-semibold text-neutral-800"
                >
                  Password
                </label>
                <div className="mt-1.5">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    value={formik.values.password}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className={`block w-full rounded-xl border bg-neutral-50/50 px-4 py-3 text-neutral-900 placeholder-neutral-400 shadow-sm transition-all focus:outline-none focus:ring-1 ${
                      formik.touched.password && formik.errors.password
                        ? "border-red-400 focus:border-red-400 focus:ring-red-400"
                        : "border-neutral-200 focus:border-green-500 focus:ring-green-500"
                    }`}
                    placeholder="••••••••"
                  />
                </div>
                {formik.touched.password && formik.errors.password && (
                  <p className="mt-1 text-xs text-red-500 font-medium">
                    {formik.errors.password}
                  </p>
                )}
              </div>
            </div>

            {/* Custom Brand Gradient Submit Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={loading || !formik.isValid}
                className={`${loading || !formik.isValid ? "cursor-not-allowed" : "cursor-pointer"} flex w-full justify-center items-center gap-1.5 rounded-xl bg-linear-to-r from-green-600 to-amber-500 px-4 py-3 text-sm font-bold text-white shadow-md hover:opacity-95 disabled:opacity-50 disabled:cursor-not-allowed transition-all`}
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <svg
                      className="h-5 w-5 animate-spin text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    <span>Signing in...</span>
                  </div>
                ) : (
                  <>
                    Log in <span>→</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Social Divider */}
          <div className="relative flex items-center justify-center">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-neutral-100"></div>
            </div>
            <span className="relative bg-white px-3 text-[11px] font-semibold text-neutral-400 uppercase tracking-wider">
              Or
            </span>
          </div>

          {/* Google Social Login */}
          <div className="flex justify-center">
            <GoogleButton />
          </div>
        </div>

        {/* Redirect Footer Link */}
        <div className="text-center text-sm font-medium text-neutral-500 pt-2">
          New here?{" "}
          <Link
            href="/register"
            className="font-bold text-green-600 hover:text-green-700 transition-colors underline underline-offset-4 decoration-2"
          >
            Create an account
          </Link>
        </div>
      </div>
    </div>
  );
}
