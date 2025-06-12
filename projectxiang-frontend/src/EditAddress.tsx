import React, { useState, useEffect } from 'react';

const EditAddress: React.FC = () => {
  const [address, setAddress] = useState({
    street: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Optionally, fetch current address here using the token
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAddress({ ...address, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/add_user_address/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ ...address }),
      });
      if (res.ok) {
        setMessage('Address updated!');
      } else {
        setMessage('Failed to update address.');
      }
    } catch (err) {
      setMessage('Failed to update address.');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Edit Address</h2>
      <form onSubmit={handleSubmit}>
        <input name="street" placeholder="Street" value={address.street} onChange={handleChange} /><br />
        <input name="city" placeholder="City" value={address.city} onChange={handleChange} /><br />
        <input name="state" placeholder="State" value={address.state} onChange={handleChange} /><br />
        <input name="zip_code" placeholder="Zip Code" value={address.zip_code} onChange={handleChange} /><br />
        <input name="country" placeholder="Country" value={address.country} onChange={handleChange} /><br />
        <button type="submit">Save Address</button>
      </form>
      {message && <div style={{ marginTop: 10 }}>{message}</div>}
    </div>
  );
};

export default EditAddress;
