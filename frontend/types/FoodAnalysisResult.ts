export interface FoodAnalysisResult {
  foodId: string;
  status: "processing" | "completed" | "failed";
  calories: number;
  protein: number;
  carbohydrates: number;
  fats: number;
  name:string;
  confidence:number;
  error?: string;
}
