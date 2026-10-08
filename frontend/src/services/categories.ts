import api from "./api";

export interface Category {
  id: string;
  name: string;
  type: "income" | "expense";
}

interface CategoryResponse {
  data: Category;
}

interface CategoriesResponse {
  data: Category[];
}

interface CreateCategoryData {
  name: string;
  type: "income" | "expense";
}

export const getCategories = async (): Promise<CategoriesResponse> => {
  const response = await api.get<CategoriesResponse>("/categories");
  return response.data;
};

export const createCategory = async (
  data: CreateCategoryData,
): Promise<CategoryResponse> => {
  const response = await api.post<CategoryResponse>("/categories", data);
  return response.data;
};

export const deleteCategory = async (id: string): Promise<void> => {
  await api.delete(`/categories/${id}`);
};
