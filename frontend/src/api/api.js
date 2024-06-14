import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Replace with your backend base URL

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add a request interceptor to include the JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const getPoints = async () => {
  try {
    const response = await apiClient.get('/points/');
    return response.data;
  } catch (error) {
    console.error('Error getting points:', error);
    throw error;
  }
};

export const createPoint = async (pointData, token) => {
  try {
    const response = await apiClient.post('/points/', pointData, {
      headers: {
        Authorization: `Bearer ${token}`  // Assuming your API expects a Bearer token
        // Add other headers if required by your API
      }
    });
    return response.data;
  } catch (error) {
    // Handle error here
    console.error('Error creating point:', error);
    throw error; // Optional: rethrow the error to handle it elsewhere
  }
};

export const updatePoint = async (pointId, newDescription, token) => {
  console.log('Updating point in api', pointId, newDescription);
  try {
    const response = await apiClient.put(`/points/${pointId}/`, { description: newDescription }, {
      headers: {
        Authorization: `Bearer ${token}`
        // Add other headers if required by your API
      }
    });
    return response.data;
  }
  catch (error) {
    console.error('Error updating point:', error);
    throw error;
  }
}



export const deletePoint = async (pointId, token) => {
  try {
    const response = await apiClient.delete(`/points/${pointId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
        // Add other headers if required by your API
      }
    });
    return response.data;
  }
  catch (error) {
    console.error('Error deleting point:', error);
    throw error;
  }
}
