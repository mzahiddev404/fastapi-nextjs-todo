// TypeScript type definitions for the TODO application
// Centralized type definitions to ensure type safety across the app

export interface User {
  id: string;
  username: string;
  email: string;
  name?: string;
  created_at?: string;
  updated_at?: string;
  is_demo?: boolean;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'incomplete' | 'complete';
  priority: 'low' | 'medium' | 'high';
  due_date: string;  // Required field
  label_ids?: string[];
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Label {
  id: string;
  name: string;
  color: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  task_count?: number; // For display purposes
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  due_date: string;  // Required field
  label_ids?: string[];
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: 'incomplete' | 'complete';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  label_ids?: string[];
}

export interface LabelCreate {
  name: string;
  color: string;
}

export interface LabelUpdate {
  name?: string;
  color?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface TaskStats {
  total: number;
  incomplete: number;
  complete: number;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}
