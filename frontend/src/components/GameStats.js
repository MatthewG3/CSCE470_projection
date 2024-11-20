import React, { useState } from 'react';

const GameStats = ({ stats }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => setIsOpen(!isOpen);

  return (
    <div>
      <button onClick={toggleDropdown} style={{ margin: '10px', padding: '5px 10px', cursor: 'pointer' }}>
        {isOpen ? 'Hide Details' : 'Show Details'}
      </button>
      {isOpen && (
        <div style={{ padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
          {stats.map((stat, index) => (
            <div key={index}>
              <strong>{stat.label}:</strong> {stat.displayValue}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GameStats;
