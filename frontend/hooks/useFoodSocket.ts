import { useEffect, useRef, useState } from "react";
import { FoodAnalysisResult } from "@/types/FoodAnalysisResult";

export const useFoodSocket = (foodId: string | null) => {
  const [data, setData] = useState<FoodAnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const socketRef = useRef<WebSocket | null>(null);

  // Function to clear the analysis result
  const clearData = () => {
    setData(null);
    setError(null);
    setIsLoading(false);
  };

  useEffect(() => {
    if (!foodId) return;

    setIsLoading(true);
    setError(null);

    // const socket = new WebSocket(`ws://127.0.0.1:8000/ws/food/${foodId}`);
    const socket = new WebSocket(`ws://localhost:8000/ws/food/${foodId}`);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log(`WebSocket connected for food item: ${foodId}`);
    };

    socket.onmessage = (event) => {
      try {
        const parsedData: FoodAnalysisResult = JSON.parse(event.data);
        setData(parsedData);

        if (
          parsedData.status === "completed" ||
          parsedData.status === "failed"
        ) {
          setIsLoading(false);
          socket.close();
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
        setError("Invalid data received from server.");
      }
    };

    socket.onerror = (event) => {
      console.error("WebSocket error observed:", event);
      setError("A connection error occurred.");
      setIsLoading(false);
    };

    socket.onclose = (event) => {
      console.log(`WebSocket closed: Code ${event.code}`);
      setIsLoading(false);
    };

    return () => {
      if (
        socket.readyState === WebSocket.OPEN ||
        socket.readyState === WebSocket.CONNECTING
      ) {
        socket.close();
      }
    };
  }, [foodId]);

  return {
    data,
    isLoading,
    error,
    clearData,
  };
};