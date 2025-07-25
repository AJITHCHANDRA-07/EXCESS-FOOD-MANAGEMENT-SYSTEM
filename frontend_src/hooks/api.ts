import React, { useEffect, useState } from 'react';
import { useApi } from '../context/ApiContext';
import { useToast } from './ui/use-toast';

// Types for API responses
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Hook for making API calls with loading and error handling
export function useApiCall<T>(endpoint: string, method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET') {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { api } = useApi();
  const { toast } = useToast();

  const makeRequest = async (payload?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      
      switch (method) {
        case 'GET':
          response = await api.get<ApiResponse<T>>(endpoint);
          break;
        case 'POST':
          response = await api.post<ApiResponse<T>>(endpoint, payload);
          break;
        case 'PUT':
          response = await api.put<ApiResponse<T>>(endpoint, payload);
          break;
        case 'DELETE':
          response = await api.delete<ApiResponse<T>>(endpoint);
          break;
      }
      
      if (response.data.success) {
        setData(response.data.data || null);
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'An unknown error occurred');
      }
    } catch (err: any) {
      const errorMessage = err.message || 'An unknown error occurred';
      setError(errorMessage);
      
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      });
      
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, makeRequest };
}

// Hook for fetching data on component mount
export function useFetchData<T>(endpoint: string) {
  const { data, loading, error, makeRequest } = useApiCall<T>(endpoint);
  
  useEffect(() => {
    makeRequest();
  }, [endpoint]);
  
  return { data, loading, error, refetch: makeRequest };
}
