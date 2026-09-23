import { apiClient } from "./api";

export const uploadImage = (formData: FormData) => {
  return apiClient.post("/food/upload", formData,{
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
export const getUserFoodHistory = ()=> apiClient.get("/food/history")
export const getImages = () => apiClient.get("/images");