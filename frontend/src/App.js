import React from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import InfoSection from './components/InfoSection';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <SearchBar />
      <InfoSection />
    </div>
  );
}

export default App;
