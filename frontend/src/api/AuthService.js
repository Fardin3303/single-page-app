import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // backend base URL

export const createUser = async (userData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/`, userData);
    return response.data;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
}

export const getTokenForUser = async (username, password) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/token/`,
      new URLSearchParams({
        username: username,
        password: password
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error getting token:', error);
    throw error;
  }
};
