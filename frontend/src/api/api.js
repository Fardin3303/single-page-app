import axios from 'axios';

const API_BASE_URL = 'http://host.docker.internal:8000'; // Replace with your backend base URL

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
  const response = await apiClient.get('/points/');
  return response.data;
};

export const createPoint = async (pointData) => {
  const response = await apiClient.post('/points/', pointData);
  return response.data;
};

export const updatePoint = async (pointId, pointData) => {
  const response = await apiClient.put(`/points/${pointId}/`, pointData);
  return response.data;
};

export const deletePoint = async (pointId) => {
  const response = await apiClient.delete(`/points/${pointId}/`);
  return response.data;
};
