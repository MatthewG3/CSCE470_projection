import React, { useState } from 'react';
import "../GameStats.css";

const GameStats = ({ stats }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => setIsExpanded(!isExpanded);

  return (
    <div className="game-stats">
      <div className="toggle-button" onClick={toggleExpand}>
        {isExpanded ? 'Hide Details' : 'Show Details'}
      </div>
      {isExpanded && (
        <div className="stats-details">
          {Object.entries(stats).map(([statLabel, teamStats]) => (
            <div key={statLabel} className="stat-group">
              <div className="stat-label">{statLabel}:</div>
              {teamStats.map(([teamName, value], index) => (
                <div key={index} className="stat-value">
                  {teamName}: {value}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GameStats;
