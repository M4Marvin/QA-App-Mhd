import React, { createContext, useState, useEffect, useContext } from "react";
import { verifyToken, getUserInfo, login as apiLogin } from "../api/api";

export const AuthContext = createContext({
  userInfo: null,
  isLoading: false,
  login: () => {},
  error: null,
  logout: () => {},
});

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("authToken");
        if (token) {
          const isTokenValid = await verifyToken(token);
          if (!isTokenValid) {
            setError("Invalid or expired token.");
            return;
          }
          const userData = await getUserInfo();
          setUserInfo(userData);
        }
      } catch (e) {
        setError("Failed to verify user information.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const login = async (email, password) => {
    try {
      const { role, token } = await apiLogin(email, password);
      localStorage.setItem("authToken", token);
      const userData = await getUserInfo();
      setUserInfo({ ...userData, role, token });
    } catch (error) {
      setError("Login failed: Invalid email or password.");
    }
  };

  const logout = () => {
    try {
      localStorage.removeItem("authToken");
      setUserInfo(null);
    } catch (error) {
      setError("Logout failed: Unable to remove token.");
    }
  };

  const value = {
    userInfo,
    isLoading,
    login,
    error,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
