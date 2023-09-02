import { Container, Box, Typography } from "@mui/material";

const AccessDenied = () => {
  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom color="red">
          Access Denied
        </Typography>
        <Typography variant="body1">
          You don't have permission to access this page.
        </Typography>
      </Box>
    </Container>
  );
};

export default AccessDenied;
