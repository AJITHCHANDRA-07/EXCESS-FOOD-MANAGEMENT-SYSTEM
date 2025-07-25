import React, { createContext, useContext, useState, ReactNode } from 'react';
import axios, { AxiosInstance } from 'axios';

// Define the API context type
interface ApiContextType {
  api: AxiosInstance;
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

// Create the context with a default value
const ApiContext = createContext<ApiContextType | undefined>(undefined);

// Custom hook to use the API context
export const useApi = () => {
  const context = useContext(ApiContext);
  if (context === undefined) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

// Props for the ApiProvider component
interface ApiProviderProps {
  children: ReactNode;
}

// API Provider component
export const ApiProvider: React.FC<ApiProviderProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Create an axios instance with default config
  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Add request interceptor
  api.interceptors.request.use(
    (config) => {
      setIsLoading(true);
      
      // Get token from localStorage if it exists
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      return config;
    },
    (error) => {
      setIsLoading(false);
      setError(error.message || 'An error occurred during the request');
      return Promise.reject(error);
    }
  );

  // Add response interceptor
  api.interceptors.response.use(
    (response) => {
      setIsLoading(false);
      return response;
    },
    (error) => {
      setIsLoading(false);
      
      // Handle different error responses
      if (error.response) {
        // Server responded with a status code outside of 2xx range
        if (error.response.status === 401) {
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_role');
          window.location.href = '/login';
        }
        
        setError(error.response.data.message || `Error ${error.response.status}: ${error.response.statusText}`);
      } else if (error.request) {
        // Request was made but no response received
        setError('No response received from server. Please check your connection.');
      } else {
        // Something else happened while setting up the request
        setError(error.message || 'An unknown error occurred');
      }
      
      return Promise.reject(error);
    }
  );

  // Function to clear error state
  const clearError = () => {
    setError(null);
  };

  // Provide the API context to children
  return (
    <ApiContext.Provider value={{ api, isLoading, error, clearError }}>
      {children}
    </ApiContext.Provider>
  );
};
