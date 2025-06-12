import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => (
  <div style={{ textAlign: 'center', marginTop: '3rem' }}>
    <h1>Welcome to ProjectXiang</h1>
    <div style={{ margin: '2rem' }}>
      <Link to="/signup" style={{ marginRight: '2rem', fontSize: '1.2rem' }}>Sign Up</Link>
      <Link to="/login" style={{ fontSize: '1.2rem' }}>Login</Link>
    </div>
  </div>
);

export default Home;
