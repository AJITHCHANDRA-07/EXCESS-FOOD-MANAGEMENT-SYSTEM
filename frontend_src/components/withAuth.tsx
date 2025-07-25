import React, { useEffect, useState } from 'react';
import { useApi } from '../context/ApiContext';
import { useToast } from './ui/use-toast';

// Higher-order component for protected routes
const withAuth = (WrappedComponent: React.ComponentType, requiredRole: 'admin' | 'volunteer') => {
  return (props: any) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const { api } = useApi();
    const { toast } = useToast();
    
    useEffect(() => {
      const checkAuth = async () => {
        const token = localStorage.getItem('auth_token');
        const userRole = localStorage.getItem('user_role');
        
        if (!token || !userRole) {
          // No token or role found, redirect to login
          setIsAuthenticated(false);
          setIsLoading(false);
          
          // Redirect to appropriate login page
          window.location.href = requiredRole === 'admin' ? '/admin/login' : '/volunteer/login';
          return;
        }
        
        if (userRole !== requiredRole) {
          // User doesn't have the required role
          toast({
            title: "Access Denied",
            description: `You need ${requiredRole} privileges to access this page.`,
            variant: "destructive",
          });
          
          // Redirect to appropriate login page
          window.location.href = requiredRole === 'admin' ? '/admin/login' : '/volunteer/login';
          return;
        }
        
        try {
          // In a real implementation, this would verify the token with the backend
          // For now, we'll just simulate a successful verification
          await new Promise(resolve => setTimeout(resolve, 500));
          
          setIsAuthenticated(true);
        } catch (error) {
          // Token verification failed
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_role');
          
          toast({
            title: "Authentication Error",
            description: "Your session has expired. Please log in again.",
            variant: "destructive",
          });
          
          // Redirect to appropriate login page
          window.location.href = requiredRole === 'admin' ? '/admin/login' : '/volunteer/login';
        } finally {
          setIsLoading(false);
        }
      };
      
      checkAuth();
    }, []);
    
    if (isLoading) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-700"></div>
        </div>
      );
    }
    
    return isAuthenticated ? <WrappedComponent {...props} /> : null;
  };
};

export default withAuth;
