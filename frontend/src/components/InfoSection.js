import React from 'react';
import '../InfoSection.css';
import nflChart from '../assets/nflchart.png';

const InfoSection = () => {
  return (
    <div className="info-section">
      <h2>Search For Anything!</h2>
      <p>
        Our system allows you to search for anything you desire regarding your NFL team.
        There's plenty to explore, such as largest comebacks from last year, most exciting games, and many more!
      </p>
      
      <img src={nflChart} alt="NFL Chart" className="chart" />
    </div>
  );
};

export default InfoSection;
