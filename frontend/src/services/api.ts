import axios from 'axios';
import { LoginData, RegisterData, Sweet, Purchase } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (data: LoginData) => api.post('/auth/login', data),
  register: (data: RegisterData) => api.post('/auth/register', data),
};

export const sweetsAPI = {
  getAll: () => api.get('/sweets'),
  getById: (id: number) => api.get(`/sweets/${id}`),
  search: (params: {
    query?: string;
    category?: string;
    min_price?: number;
    max_price?: number;
  }) => api.get('/sweets/search', { params }),
  create: (data: Omit<Sweet, 'id' | 'created_at' | 'updated_at'>) => api.post('/sweets', data),
  update: (id: number, data: Partial<Sweet>) => api.put(`/sweets/${id}`, data),
  delete: (id: number) => api.delete(`/sweets/${id}`),
  purchase: (id: number, quantity: number) => 
    api.post(`/sweets/${id}/purchase`, { quantity }),
  restock: (id: number, quantity: number) => 
    api.post(`/sweets/${id}/restock`, { quantity }),
};

export const purchasesAPI = {
  getMyPurchases: () => api.get('/purchases'),
};

export default api;