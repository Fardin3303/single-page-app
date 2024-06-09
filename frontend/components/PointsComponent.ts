import React, { useEffect, useState } from 'react';
import { getPoints, createPoint, updatePoint, deletePoint } from '../api/api';

const PointsComponent = () => {
  const [points, setPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPoints = async () => {
      try {
        const data = await getPoints();
        setPoints(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPoints();
  }, []);

  const handleAddPoint = async (pointData) => {
    try {
      const newPoint = await createPoint(pointData);
      setPoints([...points, newPoint]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdatePoint = async (pointId, updatedData) => {
    try {
      const updatedPoint = await updatePoint(pointId, updatedData);
      setPoints(points.map(point => (point.id === pointId ? updatedPoint : point)));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeletePoint = async (pointId) => {
    try {
      await deletePoint(pointId);
      setPoints(points.filter(point => point.id !== pointId));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Points of Interest</h1>
      <ul>
        {points.map(point => (
          <li key={point.id}>
            {point.description} - Created by: {point.creator}
            {/* Add buttons or forms for editing and deleting points */}
            <button onClick={() => handleUpdatePoint(point.id, { description: 'Updated description' })}>Edit</button>
            <button onClick={() => handleDeletePoint(point.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {/* Add form or button to add a new point */}
      <button onClick={() => handleAddPoint({ description: 'New Point', lat: 0, lng: 0 })}>Add Point</button>
    </div>
  );
};

export default PointsComponent;
