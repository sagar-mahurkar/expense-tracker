import api from "./api";

interface RegisterData {
  name: string;
  email: string;
  password: string;
}

interface LoginData {
  email: string;
  password: string;
}

export interface AuthUser {
  id: string;
  name: string;
  email: string;
}

interface RegisterResponse {
  data: {
    id: string;
    name: string;
    email: string;
    created_at: string;
  };
}

export interface LoginResponse {
  data: {
    access_token: string;
    user: AuthUser;
  };
}

export const register = async (
  data: RegisterData,
): Promise<RegisterResponse> => {
  const response = await api.post<RegisterResponse>("/auth/register", data);

  return response.data;
};

export const login = async (
  data: LoginData,
): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>("/auth/login", data);

  return response.data;
};
