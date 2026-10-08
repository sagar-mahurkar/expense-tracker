import api from "./api";

export interface Summary {
  balance: string;
  income: string;
  expense: string;
}

interface SummaryResponse {
  data: Summary;
}

export const getSummary = async (): Promise<SummaryResponse> => {
  const response = await api.get<SummaryResponse>("/summary");
  return response.data;
};
