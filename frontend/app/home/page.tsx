"use client";

import { useState } from "react";
import Header from "@/components/home/Header";
import ImageUpload from "@/components/home/ImageUpload";
import NutritionResults from "@/components/home/NutritionResults";
import { uploadImage } from "@/services/food";
import axios from "axios";
import { toast } from "sonner";
import { useFoodSocket } from "@/hooks/useFoodSocket";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter()
  const [activeFoodId, setActiveFoodId] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { data, isLoading, error, clearData } = useFoodSocket(activeFoodId);

  const handleFileChange = (file: File) => {
    setImageFile(file);
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };
  
  const onViewListClick = ()=>{
    router.push('/foods')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) return;

    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("image", imageFile);

    try {
      const response = await uploadImage(formData);
      toast.success(response.data.message);
      setActiveFoodId(response.data.food_item_id);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const serverError = error.response?.data;

        if (serverError) {
          console.log("Message:", serverError);
        }

        console.log("HTTP Status Code:", error.response?.status);
      } else {
        const err = error as Error;
        console.log("Error Message:", err.message);
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-[#F9FBF9] text-neutral-800 min-h-screen font-sans antialiased">
      <Header />

      {/* Styled to host the wide two-column grid structure cleanly */}
      <main className="max-w-7xl mx-auto px-6 md:px-16 py-12 space-y-10">
        
        {/* Intro Banner Section Matching image_f30d25.png layout */}
        <section className="text-left max-w-xl space-y-2">
          <h1 className="text-4xl font-extrabold text-neutral-950 tracking-tight">
            Analyze a meal
          </h1>
          <p className="text-neutral-500 text-base font-medium">
            Upload a food image and let our AI break down its nutrients.
          </p>
        </section>
        <div className="w-full flex gap-5">
          {/* Upload Form Component */}
          <ImageUpload
            imagePreview={imagePreview}
            onFileChange={handleFileChange}
            onSubmit={handleSubmit}
            onClear={() => {
              setImageFile(null);
              setImagePreview(null);
              clearData();
            }}
            isAnalyzing={isAnalyzing}
            isFoodProcesssing={isLoading}
            hasFile={!!imageFile}
            onViewListClick={onViewListClick}
          />

          {/* Dynamic Nutrition Display */}
          {data && <NutritionResults data={data} />}
        </div>
      </main>
    </div>
  );
}