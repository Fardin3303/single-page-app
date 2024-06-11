// src/Components/Points/PointForm.js
import React, { useState } from 'react';
import { createPoint } from '../../api/api';
import { useNavigate } from 'react-router-dom';

const PointForm = () => {
  const [description, setDescription] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createPoint({ description });
      navigate('/points');
    } catch (error) {
      console.error('Failed to create point', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" required />
      <button type="submit">Create Point</button>
    </form>
  );
};

export default PointForm;
