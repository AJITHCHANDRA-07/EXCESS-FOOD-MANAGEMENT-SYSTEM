import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from './components/ui/toaster';

// Components
import HomePage from './components/HomePage';
import MachineLocator from './components/MachineLocator';
import AdminDashboard from './components/AdminDashboard';
import VolunteerPortal from './components/VolunteerPortal';
import AdminLogin from './components/AdminLogin';
import VolunteerLogin from './components/VolunteerLogin';

// API Context
import { ApiProvider } from './context/ApiContext';

function App() {
  return (
    <ApiProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/locate" element={<MachineLocator />} />
          
          {/* Auth Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/volunteer/login" element={<VolunteerLogin />} />
          
          {/* Protected Routes */}
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/volunteer/portal" element={<VolunteerPortal />} />
          
          {/* Fallback Route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <Toaster />
      </Router>
    </ApiProvider>
  );
}

export default App;
