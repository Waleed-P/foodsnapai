export interface HistoryItem {
  id:number;
  name:string;
  created_at: string;
  image_url:string;
  status:string;
  protein:number;
  fats:number;
  carbohydrates:number;
  calories:number;
  confidence:number;
  
}
export interface FoodHistoryResult {
  data: {
    history: HistoryItem[];
  };
}
