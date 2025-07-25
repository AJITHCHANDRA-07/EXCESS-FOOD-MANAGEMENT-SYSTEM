import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { useToast } from './ui/use-toast';
import { useApi } from '../context/ApiContext';

const VolunteerLogin: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { api, error, clearError } = useApi();
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      toast({
        title: "Error",
        description: "Please enter both email and password",
        variant: "destructive",
      });
      return;
    }
    
    setIsSubmitting(true);
    clearError();
    
    try {
      // In a real implementation, this would call the backend API
      // For now, we'll simulate a successful login with volunteer credentials
      if (email === 'volunteer@example.com' && password === 'volunteer123') {
        // Simulate API response delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Store auth token and user role
        localStorage.setItem('auth_token', 'mock_volunteer_token');
        localStorage.setItem('user_role', 'volunteer');
        
        toast({
          title: "Success",
          description: "You have successfully logged in as a volunteer",
        });
        
        // Redirect to volunteer portal
        navigate('/volunteer/portal');
      } else {
        // Simulate failed login
        throw new Error('Invalid credentials');
      }
    } catch (err) {
      toast({
        title: "Login Failed",
        description: error || "Invalid email or password. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-4">
        <Card>
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center text-blue-600">Volunteer Login</CardTitle>
            <CardDescription className="text-center">
              Enter your credentials to access the volunteer portal
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="email" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Email
                  </label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="volunteer@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="password" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Password
                  </label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <Button 
                  type="submit" 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                      Signing in...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
          <CardFooter className="flex flex-col">
            <p className="text-xs text-center text-gray-500 mt-4">
              For demo purposes, use: volunteer@example.com / volunteer123
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default VolunteerLogin;
