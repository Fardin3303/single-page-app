import axios from 'axios';

const API_BASE_URL = 'http://host.docker.internal:8000'; // backend base URL

export const login = async (username: string, password: string) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, { username, password });
  const { token } = response.data;
  localStorage.setItem('token', token);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};
