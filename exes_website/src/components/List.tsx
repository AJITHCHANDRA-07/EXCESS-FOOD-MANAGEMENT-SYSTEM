import React from 'react';

interface ListItemProps {
  children: React.ReactNode;
  bold?: boolean;
}

const ListItem: React.FC<ListItemProps> = ({ children, bold = false }) => {
  return (
    <li className={`mb-2 ${bold ? 'font-semibold' : ''}`}>
      {children}
    </li>
  );
};

const List: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ul className="list-disc pl-6 my-3 space-y-1">
      {children}
    </ul>
  );
};

export { List, ListItem };
