import React from 'react';
import '../Header.css';
import nflLogo from '../assets/nfl_logo.svg';

const Header = () => {
  return (
    <header className="header">
      <img src={nflLogo} alt="NFL Logo" className="logo" />
      <h1>NFL Gridiron Guru</h1>
    </header>
  );
};

export default Header;
