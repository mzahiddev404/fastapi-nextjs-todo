// Custom hook for label management using SWR
import useSWR from "swr";
import { Label, LabelCreate, LabelUpdate } from "@/types";
import { api } from "@/lib/apiClient";

// Response type from backend for label list
interface LabelListResponse {
  labels: Label[];
  total: number;
}

// Fetcher function for SWR
const fetcher = async (url: string): Promise<Label[]> => {
  const response = await api.get<LabelListResponse>(url);
  return response.labels; // Extract labels array from response
};

export function useLabels() {
  // Fetch all labels
  const { data: labels, error, isLoading, mutate } = useSWR(
    "/api/v1/labels",
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 60000, // Cache for 1 minute
    }
  );

  // Create a new label
  const createLabel = async (labelData: LabelCreate) => {
    try {
      const newLabel = await api.post<Label>("/api/v1/labels", labelData);
      mutate(); // Revalidate labels list
      return newLabel;
    } catch (error) {
      throw error;
    }
  };

  // Update a label
  const updateLabel = async (labelId: string, labelData: LabelUpdate) => {
    try {
      const updatedLabel = await api.put<Label>(`/api/v1/labels/${labelId}`, labelData);
      mutate(); // Revalidate labels list
      return updatedLabel;
    } catch (error) {
      throw error;
    }
  };

  // Delete a label
  const deleteLabel = async (labelId: string) => {
    try {
      await api.delete(`/api/v1/labels/${labelId}`);
      mutate(); // Revalidate labels list
    } catch (error) {
      throw error;
    }
  };

  return {
    labels: labels || [],
    isLoading,
    error,
    createLabel,
    updateLabel,
    deleteLabel,
    mutate,
  };
}
