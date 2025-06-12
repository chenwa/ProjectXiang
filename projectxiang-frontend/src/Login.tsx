import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API_BASE_URL from './config';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);
      const res = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form.toString(),
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        navigate('/edit-address');
      } else {
        setError('Login failed.');
      }
    } catch (err) {
      setError('Login failed.');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input name="email" type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required /><br />
        <input name="password" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required /><br />
        <button type="submit">Login</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
    </div>
  );
};

export default Login;
