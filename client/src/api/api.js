// src/api/api.js
// Functions to make API calls to the backend
import axios from "axios";

const BASE_URL = "http://localhost:5000";

const api = axios.create({
  baseURL: BASE_URL,
});

// Verify token
// This function will be used to verify the token that is stored in localStorage. before making any API calls.
export const verifyToken = async (token) => {
  try {
    const response = await api.get("/verify-token", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // If the token is valid, 200 is the status code that is returned.
    return response.status === 200;
  } catch (error) {
    console.log(error);
  }
};

// Login
export const login = async (email, password) => {
  try {
    const response = await api.post("/login", {
      email,
      password,
    });
    const { role, token } = response.data;
    localStorage.setItem("authToken", token);
    return { role, token };
  } catch (error) {
    console.log(error);
  }
};

// Get token
export const getToken = () => {
  return localStorage.getItem("authToken");
};

// Upload csv file
export const uploadFile = async (file) => {
  const token = getToken();
  if (!token) {
    throw new Error("No token found. Please log in.");
  }

  try {
    const formData = new FormData();
    formData.append("file", file);

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
      },
    };

    const response = await api.post("/upload-scores-csv", formData, config);

    if (response.status !== 200) {
      throw new Error(response.data.message);
    }

    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.message || error.message;
    console.error("Upload failed:", errorMessage);
    throw new Error(errorMessage);
  }
};

// Get user info
export const getUserInfo = async () => {
  try {
    // Verify token before making API call
    const token = getToken();
    const isTokenValid = await verifyToken(token);
    if (!isTokenValid) {
      throw new Error("Invalid token");
    }

    const response = await api.get("/user", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

// Get professors
export const getProfessors = async () => {
  try {
    // Verify token before making API call
    const token = getToken();
    const isTokenValid = await verifyToken(token);
    if (!isTokenValid) {
      throw new Error("Invalid token");
    }

    const response = await api.get("/professors", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

// Get grades
export const getScores = async () => {
  try {
    const token = getToken(); // Get token from local storage or cookie
    if (!token) {
      throw new Error("No token found. Please log in.");
    }

    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    const response = await axios.get("/get-scores", config);

    if (response.status === 200) {
      return response.data.scores;
    } else {
      throw new Error("Failed to get scores.");
    }
  } catch (error) {
    console.error("An error occurred while fetching data: ", error);
    throw error;
  }
};
