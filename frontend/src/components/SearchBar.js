import React, { useState } from 'react';
import Card from './Card';
import '../SearchBar.css';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearch = () => {
    fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.results);
        setResults(data.results);
      })
      .catch(error => {
        console.error('Error fetching data: ', error);
      });
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Search..."
        className="search-input"
      />
      <button className="search-button" onClick={handleSearch}>Search</button>
      <div>
        {results.map((game, index) => (
          <Card key={index} game={game} />
        ))}
      </div>
    </div>
  );
};

export default SearchBar;
