import axios from "axios";
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;
    const url = originalRequest?.url || "";

    console.log("❌ API Response Error encountered:", {
      url: url,
      status: status || "Network Error/No Response",
    });

    // 🛑 Rule 1: If the token refresh OR logout request itself fails with a 401,
    // don't try to refresh again. Break out immediately.
    if (status === 401 && (url.includes("/auth/refresh") || url.includes("/auth/logout"))) {
      isRefreshing = false;
      console.warn("🚨 Auth system failure (Expired refresh session or forced logout). rejecting promise...");
      return Promise.reject(error);
    }

    if (status === 401) {
      console.warn("🔒 Status is 401 (Unauthorized). Attempting token refresh...");
    }

    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        if (!isRefreshing) {
          isRefreshing = true;
          console.log("🔄 Firing /auth/refresh request...");
          await apiClient.post("/auth/refresh");
          isRefreshing = false;
          console.log("✅ Token refresh successful!");
        }

        console.log(`🔁 Retrying original request: ${url}`);
        return apiClient(originalRequest);
      } catch (refreshError) {
        isRefreshing = false; 
        console.log("🚨 Token refresh failed. Triggering server logout api call...");

        try {
          // 🔄 Call your backend logout endpoint to clear server-side cookies/sessions
          await apiClient.post("/auth/logout");
        } catch (logoutBackendError) {
          console.log("Failed to cleanly clear server session:", logoutBackendError);
        }

        // Pass the error back up to your AuthProvider to handle the client-side redirect
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);