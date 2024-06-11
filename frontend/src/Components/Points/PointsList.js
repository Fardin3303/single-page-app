// src/Components/Points/PointsList.js
import React, { useEffect, useState } from 'react';
import { getPoints, deletePoint } from '../../api/api';
import { useNavigate } from 'react-router-dom';

const PointsList = () => {
  const [points, setPoints] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPoints = async () => {
      try {
        const data = await getPoints();
        setPoints(data);
      } catch (error) {
        console.error('Failed to fetch points', error);
      }
    };
    fetchPoints();
  }, []);

  const handleDelete = async (id) => {
    try {
      await deletePoint(id);
      setPoints(points.filter(point => point.id !== id));
    } catch (error) {
      console.error('Failed to delete point', error);
    }
  };

  return (
    <div>
      <h2>Points List</h2>
      <button onClick={() => navigate('/create-point')}>Create Point</button>
      <ul>
        {points.map(point => (
          <li key={point.id}>
            {point.description}
            <button onClick={() => handleDelete(point.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PointsList;
