import { apiClient } from "./api";

export const register = (name: string, email: string, password: string) =>
  apiClient.post("/auth/register", {
    name,
    email,
    password,
  });

export const login = (email: string, password: string) =>
  apiClient.post("/auth/login", {
    email,
    password,
  });

export const logout = () => apiClient.post("/auth/logout");

export const getMe = () => apiClient.get("/auth/get_me");

export const refreshToken = () => apiClient.post("/auth/refresh");
