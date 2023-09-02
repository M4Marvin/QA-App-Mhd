// ScoresPage.js
import React, { useState, useEffect } from "react";
import { getScores } from "../api/api";
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Typography,
  Box,
} from "@mui/material";
import WithRole from "./WithRole";

const ScoresPage = () => {
  const [scores, setScores] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { scores } = await getScores(); // Destructure scores from response
        setScores(scores);
        setLoading(false);
      } catch (error) {
        console.error("An error occurred while fetching data: ", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h2" gutterBottom>
          Your Scores
        </Typography>

        {loading ? (
          <CircularProgress />
        ) : scores?.length > 0 ? (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Score Value</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Objection</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {scores.map((score) => (
                  <TableRow key={score.id}>
                    <TableCell component="th" scope="row">
                      {score.id}
                    </TableCell>
                    <TableCell>{score.score_value}</TableCell>
                    <TableCell>{score.status}</TableCell>
                    <TableCell>{score.objection || "N/A"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        ) : (
          <Typography variant="body1">No scores found.</Typography>
        )}
      </Box>
    </Container>
  );
};

const ProtectedGrades = WithRole(ScoresPage, ["Professor"]);

export default ProtectedGrades;
