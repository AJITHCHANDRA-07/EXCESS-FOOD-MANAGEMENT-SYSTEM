import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-blue-600 text-white py-8 px-4 md:px-8">
      <div className="container mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-2">Exes Food Management System</h1>
        <p className="text-xl opacity-90">Integration Status Report</p>
      </div>
    </header>
  );
};

export default Header;
