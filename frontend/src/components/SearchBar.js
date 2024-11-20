import React from 'react';
import '../SearchBar.css';

const SearchBar = () => {
  return (
    <div className="search-bar">
      <input type="text" placeholder="Search..." className="search-input" />
      <button className="search-button">🔍</button>
    </div>
  );
};

export default SearchBar;
