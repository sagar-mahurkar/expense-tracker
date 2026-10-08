import api from "./api";

export interface Transaction {
  id: string;
  type: "income" | "expense";
  amount: string;
  category_id: string;
  description: string | null;
  transaction_date: string;
}

export interface TransactionInput {
  type: "income" | "expense";
  amount: string;
  category_id: string;
  description?: string;
  transaction_date: string;
}

export interface TransactionPagination {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface TransactionsResponse {
  data: Transaction[];
  pagination: TransactionPagination;
}

interface TransactionResponse {
  data: Transaction;
}

export const getTransactions = async (
  params: {
    type?: string;
    search?: string;
    start_date?: string;
    end_date?: string;
    page?: number;
    per_page?: number;
  } = {},
): Promise<TransactionsResponse> => {
  const response = await api.get<TransactionsResponse>("/transactions", {
    params,
  });

  return response.data;
};

export const createTransaction = async (
  data: TransactionInput,
): Promise<TransactionResponse> => {
  const response = await api.post<TransactionResponse>(
    "/transactions",
    data,
  );

  return response.data;
};

export const updateTransaction = async (
  id: string,
  data: TransactionInput,
): Promise<TransactionResponse> => {
  const response = await api.put<TransactionResponse>(
    `/transactions/${id}`,
    data,
  );

  return response.data;
};

export const deleteTransaction = async (id: string): Promise<void> => {
  await api.delete(`/transactions/${id}`);
};
