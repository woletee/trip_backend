import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RecommendComponent from './RecommendComponent';
import Restaurant from './Restaurant';

function App() {
  return (
    <Router>
      <div>
        <h1>Restaurant Finder</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recommend" element={<RecommendComponent />} />
          <Route path="/restaurant" element={<Restaurant />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h2>Home</h2>
      <p>Welcome to Restaurant Finder! Click the button below to get restaurant recommendations.</p>
      <button onClick={() => window.location.href = '/recommend'}>Get Recommendations</button>
    </div>
  );
}

export default App;
