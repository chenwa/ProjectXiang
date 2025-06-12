import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup: React.FC = () => {
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    street: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!form.first_name || !form.last_name || !form.email || !form.password) {
      setError('First name, last name, email, and password are required.');
      return;
    }
    try {
      const user = {
        first_name: form.first_name,
        last_name: form.last_name,
        email: form.email,
        password: form.password,
      };
      const address = form.street || form.city || form.state || form.zip_code || form.country
        ? {
            user_id: 0, // backend will link by email
            street: form.street,
            city: form.city,
            state: form.state,
            zip_code: form.zip_code,
            country: form.country,
          }
        : null;
      const res = await fetch('http://localhost:8000/users_create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user, address }),
      });
      if (res.ok) {
        navigate('/login');
      } else {
        setError('Sign up failed.');
      }
    } catch (err) {
      setError('Sign up failed.');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input name="first_name" placeholder="First Name*" value={form.first_name} onChange={handleChange} required /><br />
        <input name="last_name" placeholder="Last Name*" value={form.last_name} onChange={handleChange} required /><br />
        <input name="email" type="email" placeholder="Email*" value={form.email} onChange={handleChange} required /><br />
        <input name="password" type="password" placeholder="Password*" value={form.password} onChange={handleChange} required /><br />
        <input name="street" placeholder="Street" value={form.street} onChange={handleChange} /><br />
        <input name="city" placeholder="City" value={form.city} onChange={handleChange} /><br />
        <input name="state" placeholder="State" value={form.state} onChange={handleChange} /><br />
        <input name="zip_code" placeholder="Zip Code" value={form.zip_code} onChange={handleChange} /><br />
        <input name="country" placeholder="Country" value={form.country} onChange={handleChange} /><br />
        <button type="submit">Sign Up</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
    </div>
  );
};

export default Signup;
