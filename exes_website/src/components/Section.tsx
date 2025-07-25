import React from 'react';

interface SectionProps {
  title: string;
  children: React.ReactNode;
}

const Section: React.FC<SectionProps> = ({ title, children }) => {
  return (
    <section className="mb-10">
      <h2 className="text-2xl font-bold mb-4 text-blue-700 border-b pb-2">{title}</h2>
      <div className="pl-2">{children}</div>
    </section>
  );
};

export default Section;
