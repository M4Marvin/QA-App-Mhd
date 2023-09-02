import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Logout = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    logout();
    navigate("/"); // Redirect to home page
  }, [logout, navigate]);

  return <div>Logging out...</div>;
};

export default Logout;
