import React from 'react';
import GameStats from './GameStats';
import "../Card.css";

const Card = ({ game }) => {
  return (
    <div className="card">
      <h2>Matchup: {game[1]}</h2>
      <a href={`https://www.espn.com/nfl/boxscore/_/gameId/${game[0]}`} target="_blank">more</a>
      {/* <GameStats stats={game[4].statistics} /> */}
    </div>
  );
};

export default Card;
