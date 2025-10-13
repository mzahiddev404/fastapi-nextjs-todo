/**
 * @jest-environment jsdom
 */

import { renderHook, act, waitFor } from '@testing-library/react';
import { useAuth } from '../useAuth';
import { api } from '@/lib/apiClient';

// Mock the api client
jest.mock('@/lib/apiClient', () => ({
  api: {
    post: jest.fn(),
    get: jest.fn(),
  },
}));

// Mock SWR
jest.mock('swr', () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('useAuth Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
  });

  it('should initialize with no user when no token', () => {
    const { result } = renderHook(() => useAuth());
    
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.isLoading).toBe(false);
  });

  it('should initialize with user when token exists', () => {
    const mockToken = 'mock-jwt-token';
    const mockUser = { id: '1', email: 'test@example.com', username: 'testuser' };
    
    localStorageMock.getItem.mockReturnValue(mockToken);
    
    // Mock SWR to return user data
    const mockSWR = require('swr').default;
    mockSWR.mockReturnValue({
      data: mockUser,
      error: null,
      isLoading: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useAuth());
    
    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.isLoading).toBe(false);
  });

  it('should handle signup successfully', async () => {
    const mockToken = { access_token: 'mock-token', token_type: 'bearer' };
    const mockUser = { id: '1', email: 'test@example.com', username: 'testuser' };
    
    (api.post as jest.Mock).mockResolvedValue(mockToken);
    
    const { result } = renderHook(() => useAuth());
    
    await act(async () => {
      await result.current.signup({
        username: 'testuser',
        email: 'test@example.com',
        password: 'TestPassword123!',
      });
    });
    
    expect(api.post).toHaveBeenCalledWith('/api/v1/auth/signup', {
      username: 'testuser',
      email: 'test@example.com',
      password: 'TestPassword123!',
    });
    expect(localStorageMock.setItem).toHaveBeenCalledWith('todo_token', 'mock-token');
  });

  it('should handle signup error', async () => {
    const mockError = new Error('Email already registered');
    (api.post as jest.Mock).mockRejectedValue(mockError);
    
    const { result } = renderHook(() => useAuth());
    
    await act(async () => {
      try {
        await result.current.signup({
          username: 'testuser',
          email: 'test@example.com',
          password: 'TestPassword123!',
        });
      } catch (error) {
        expect(error).toBe(mockError);
      }
    });
  });

  it('should handle login successfully', async () => {
    const mockToken = { access_token: 'mock-token', token_type: 'bearer' };
    
    (api.post as jest.Mock).mockResolvedValue(mockToken);
    
    const { result } = renderHook(() => useAuth());
    
    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'TestPassword123!',
      });
    });
    
    expect(api.post).toHaveBeenCalledWith('/api/v1/auth/login', {
      email: 'test@example.com',
      password: 'TestPassword123!',
    });
    expect(localStorageMock.setItem).toHaveBeenCalledWith('todo_token', 'mock-token');
  });

  it('should handle login error', async () => {
    const mockError = new Error('Invalid credentials');
    (api.post as jest.Mock).mockRejectedValue(mockError);
    
    const { result } = renderHook(() => useAuth());
    
    await act(async () => {
      try {
        await result.current.login({
          email: 'test@example.com',
          password: 'wrongpassword',
        });
      } catch (error) {
        expect(error).toBe(mockError);
      }
    });
  });

  it('should handle logout', () => {
    const { result } = renderHook(() => useAuth());
    
    act(() => {
      result.current.logout();
    });
    
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('todo_token');
  });

  it('should handle authentication error', () => {
    const mockError = new Error('Authentication failed');
    
    // Mock SWR to return error
    const mockSWR = require('swr').default;
    mockSWR.mockReturnValue({
      data: null,
      error: mockError,
      isLoading: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useAuth());
    
    expect(result.current.error).toBe(mockError);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should handle loading state', () => {
    // Mock SWR to return loading state
    const mockSWR = require('swr').default;
    mockSWR.mockReturnValue({
      data: null,
      error: null,
      isLoading: true,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useAuth());
    
    expect(result.current.isLoading).toBe(true);
    expect(result.current.user).toBeNull();
  });
});
