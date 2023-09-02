import React from "react";
import { useAuth } from "../contexts/AuthContext";
import { Container, Box, Typography, CircularProgress } from "@mui/material";

function Home() {
  const { userInfo, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Container maxWidth="sm">
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
        >
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (userInfo) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ my: 4 }}>
          <Typography variant="h2" component="h1" gutterBottom>
            Welcome, {userInfo.name}
          </Typography>
          <Typography variant="body1">Name: {userInfo.name}</Typography>
          <Typography variant="body1">Role: {userInfo.role}</Typography>
          <Typography variant="body1">
            Department: {userInfo.department}
          </Typography>
          <Typography variant="body1">Email: {userInfo.email}</Typography>
        </Box>
      </Container>
    );
  } else {
    return (
      <Container maxWidth="sm">
        <Box sx={{ my: 4 }}>
          <Typography variant="body1">
            You need to log in to see the dashboard.
          </Typography>
        </Box>
      </Container>
    );
  }
}

export default Home;
