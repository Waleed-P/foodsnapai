"use client";

import { useRef } from "react";

interface ImageUploadProps {
  imagePreview: string | null;
  onFileChange: (file: File) => void;
  onSubmit: (e: React.FormEvent) => void;
  isAnalyzing: boolean;
  hasFile: boolean;
  isFoodProcesssing: boolean;
  onClear: () => void;
  onViewListClick?: () => void; 
}

export default function ImageUpload({
  imagePreview,
  onFileChange,
  onSubmit,
  onClear,
  isAnalyzing,
  hasFile,
  isFoodProcesssing,
  onViewListClick,
}: ImageUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const triggerFileInput = (captureMode?: string) => {
    if (fileInputRef.current) {
      if (captureMode === "environment") {
        fileInputRef.current.setAttribute("capture", "environment");
      } else {
        fileInputRef.current.removeAttribute("capture");
      }
      fileInputRef.current.click();
    }
  };

  const handleNativeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileChange(e.target.files[0]);
    }
  };

  const handleClear = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    onClear();
  };

  return (
    <div className="w-full max-w-xl space-y-4">
      {/* Container matching the extra rounded style with clean thin borders */}
      <section className="bg-white rounded-[2rem] shadow-sm border border-neutral-100/70 p-8">
        <form onSubmit={onSubmit} className="space-y-6">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleNativeChange}
            accept="image/*"
            className="hidden"
          />

          {/* Clickable Drag & Drop Zone Container matching image_f30d25.png */}
          <div
            onClick={() => triggerFileInput()}
            className="border border-dashed border-neutral-200 hover:border-green-500 rounded-2xl p-10 text-center cursor-pointer transition-all bg-[#F9FBF9]/40 flex flex-col items-center justify-center min-h-[260px] group"
          >
            {!imagePreview ? (
              <div className="space-y-3 flex flex-col items-center">
                {/* Cloud Upload Icon matching image_f30d25.png */}
                <div className="text-green-600 transition-transform group-hover:-translate-y-0.5">
                  <svg
                    className="w-12 h-12"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
                    />
                  </svg>
                </div>

                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-neutral-800">
                    Drop your meal photo here
                  </h3>
                  <p className="text-sm text-neutral-400 font-medium">
                    or click to browse · JPG, PNG up to 10MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4 w-full relative">
                <img
                  src={imagePreview}
                  alt="Food Preview"
                  className="max-h-64 mx-auto rounded-xl object-cover shadow-sm"
                />
                <p className="text-xs text-neutral-400 font-semibold uppercase tracking-wider">
                  Image selected successfully
                </p>

                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleClear();
                  }}
                  className="absolute -top-2 -right-2 p-1.5 bg-neutral-900/80 hover:bg-red-500 text-white rounded-full transition-colors shadow-sm"
                  title="Remove image"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2.5"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            )}
          </div>

          {/* Form Action Controls */}
          <div>
            {!isFoodProcesssing ? (
              <div className="flex items-center gap-5">
                <button
                  type="submit"
                  disabled={!hasFile || isAnalyzing}
                  className="flex justify-center items-center gap-2 rounded-xl bg-linear-to-r from-green-600 to-amber-500 px-6 py-3.5 text-sm font-bold text-white shadow-md hover:opacity-95 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                >
                  {isAnalyzing ? (
                    <>
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
                      <span>Uploading Image...</span>
                    </>
                  ) : (
                    <>
                      <span>✨</span> Analyze
                    </>
                  )}
                </button>
                <div className="text-sm text-neutral-400 font-medium">Detects 101 food categories. <span className=" text-green-600 cursor-pointer" onClick={onViewListClick}>See list ..</span></div>
              </div>
            ) : (
              /* Custom shimmer processing visual component block matching active state tracking */
              <div className="relative overflow-hidden inline-flex items-center gap-3 bg-linear-to-r from-green-600 to-emerald-500 text-white font-bold px-6 py-3.5 rounded-xl shadow-md">
                <div className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-linear-to-r from-transparent via-white/20 to-transparent"></div>
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
                <span className="relative z-10 text-sm">
                  AI is processing your food...
                </span>
              </div>
            )}
          </div>
        </form>
      </section>
    </div>
  );
}
