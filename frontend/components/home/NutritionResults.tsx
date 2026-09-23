import { FoodAnalysisResult } from "@/types/FoodAnalysisResult";

export default function NutritionResults({
  data,
}: {
  data: FoodAnalysisResult;
}) {
  // Gracefully render nothing if the API status is not completed yet
  if (data?.status !== "completed") return null;

  // Helper to map out macro ratios visually against a baseline metric target
  const getPercent = (val: number, max: number) =>
    Math.min((val / max) * 100, 100);

  const isLowConfidence = data.confidence < 80;

  return (
    <div className="w-full max-w-xl space-y-4 animate-fadeIn">
      {/* Primary Card View Container Styled like image_f32022.png */}
      <section className="bg-white rounded-[2rem] shadow-sm border border-neutral-100/70 p-8 space-y-6">
        
        {/* Dynamic Header Block Context */}
        <div className="flex items-start justify-between">
          <div className="space-y-0.5">
            <span className="text-xs font-bold text-green-600 uppercase tracking-widest">
              Detected
            </span>
            <h2 className="text-3xl font-extrabold text-neutral-950 capitalize">
              {data.name}
            </h2>
          </div>

          {/* Dynamic Confidence Score Status Badge Component */}
          <div className="flex flex-col items-end gap-1">
            <div
              className={`px-3 py-1.5 rounded-full text-xs font-medium tracking-wide border ${
                isLowConfidence
                  ? "bg-linear-to-r from-red-600 to-red-400 text-white"
                  : "bg-linear-to-r from-green-600 to-green-400 text-white"
              }`}
            >
              {isLowConfidence ? "Low confidence" : "High confidence"} ({data.confidence}%)
            </div>
          </div>
        </div>

        {/* 2x3 Grid Section Mapping Nutrients with Custom Styled Metric Card Components */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          
          {/* Calories Display Item */}
          <div className="bg-neutral-50/50 border border-neutral-100/80 rounded-2xl p-4 flex flex-col justify-between min-h-[105px]">
            <span className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider">
              Calories
            </span>
            <div className="flex items-baseline gap-1 mt-2 mb-3">
              <span className="text-2xl font-extrabold text-neutral-900">{data.calories}</span>
              <span className="text-xs font-semibold text-neutral-500">kcal</span>
            </div>
            <div className="w-full bg-neutral-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-linear-to-r from-green-500 to-amber-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${getPercent(Number(data.calories || 0), 800)}%` }}
              ></div>
            </div>
          </div>

          {/* Protein Display Item */}
          <div className="bg-neutral-50/50 border border-neutral-100/80 rounded-2xl p-4 flex flex-col justify-between min-h-[105px]">
            <span className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider">
              Protein
            </span>
            <div className="flex items-baseline gap-1 mt-2 mb-3">
              <span className="text-2xl font-extrabold text-neutral-900">{data.protein}</span>
              <span className="text-xs font-semibold text-neutral-500">g</span>
            </div>
            <div className="w-full bg-neutral-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-linear-to-r from-green-500 to-emerald-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${getPercent(Number(data.protein || 0), 50)}%` }}
              ></div>
            </div>
          </div>

          {/* Carbohydrates Display Item */}
          <div className="bg-neutral-50/50 border border-neutral-100/80 rounded-2xl p-4 flex flex-col justify-between min-h-[105px]">
            <span className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider">
              Carbs
            </span>
            <div className="flex items-baseline gap-1 mt-2 mb-3">
              <span className="text-2xl font-extrabold text-neutral-900">{data.carbohydrates}</span>
              <span className="text-xs font-semibold text-neutral-500">g</span>
            </div>
            <div className="w-full bg-neutral-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-linear-to-r from-green-500 to-amber-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${getPercent(Number(data.carbohydrates || 0), 100)}%` }}
              ></div>
            </div>
          </div>

          {/* Fat Display Item */}
          <div className="bg-neutral-50/50 border border-neutral-100/80 rounded-2xl p-4 flex flex-col justify-between min-h-[105px]">
            <span className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider">
              Fat
            </span>
            <div className="flex items-baseline gap-1 mt-2 mb-3">
              <span className="text-2xl font-extrabold text-neutral-900">{data.fats}</span>
              <span className="text-xs font-semibold text-neutral-500">g</span>
            </div>
            <div className="w-full bg-neutral-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-linear-to-r from-green-500 to-amber-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${getPercent(Number(data.fats || 0), 50)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </section>

      {/* Accuracy Warning Banner Placement Context */}
      {isLowConfidence && (
        <div className="bg-red-50/60 border border-red-100/70 text-red-800 p-4 rounded-2xl text-xs font-medium space-y-1">
          <p className="font-bold text-red-900 flex items-center gap-1">
            ⚠️ Accuracy Warning Disclaimer
          </p>
          <p className="leading-relaxed opacity-90">
            The target meal details might be incorrect. Please check our supported food categories. 
            If your food is outside that coverage matrix, system output results might be inaccurate.
          </p>
        </div>
      )}
    </div>
  );
}