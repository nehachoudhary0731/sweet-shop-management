export interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_admin: boolean;
  created_at: string;
}

export interface Sweet {
  id: number;
  name: string;
  description: string | null;
  category: string;
  price: number;
  quantity: number;
  image_url: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Purchase {
  id: number;
  user_id: number;
  sweet_id: number;
  quantity: number;
  total_price: number;
  created_at: string;
  sweet: Sweet;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}