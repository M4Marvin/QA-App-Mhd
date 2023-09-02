import React, { useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

const WithRole = (WrappedComponent, roles) => {
  const WithRoleWrapper = (props) => {
    const { userInfo } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
      if (!userInfo) {
        navigate("/login");
        return;
      }

      if (!roles) {
        return <WrappedComponent {...props} />;
      }
      if (!Array.isArray(roles)) {
        roles = [roles];
      }

      if (!roles.includes(userInfo.role)) {
        navigate("/access-denied");
      }
    }, [userInfo, navigate]);

    if (!userInfo || !roles.includes(userInfo.role)) {
      return (
        <Container maxWidth="sm">
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" component="div">
              You don't have permission to access this page.
            </Typography>
          </Box>
        </Container>
      );
    }

    return <WrappedComponent {...props} />;
  };

  return WithRoleWrapper;
};

export default WithRole;
