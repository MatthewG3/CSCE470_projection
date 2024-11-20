import React from 'react';
import '../InfoSection.css';

const InfoSection = () => {
  return (
    <div className="info-section">
      <h2>Search For Anything!</h2>
      <p>
        Our system allows you to search for anything you desire regarding your NFL team.
        There's plenty to explore, such as largest comebacks from last year, most exciting games, and many more!
      </p>
      
      <img
        src="https://via.placeholder.com/300" // Replace with your actual image or graph
        alt="Graph Placeholder"
        className="info-graph"
      />
    </div>
  );
};

export default InfoSection;
