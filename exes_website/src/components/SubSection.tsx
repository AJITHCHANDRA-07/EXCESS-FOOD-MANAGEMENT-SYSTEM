import React from 'react';

interface SubSectionProps {
  title: string;
  children: React.ReactNode;
}

const SubSection: React.FC<SubSectionProps> = ({ title, children }) => {
  return (
    <div className="mb-6">
      <h3 className="text-xl font-semibold mb-3 text-blue-600">{title}</h3>
      <div className="pl-2">{children}</div>
    </div>
  );
};

export default SubSection;
