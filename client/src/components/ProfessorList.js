import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { getProfessors } from "../api/api";
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";
import WithRole from "./WithRole";

const ProfessorList = () => {
  const [professors, setProfessors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const { userInfo } = useAuth();

  useEffect(() => {
    const fetchProfessors = async () => {
      try {
        const data = await getProfessors();

        setProfessors(data.professors);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfessors();
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Professors in the {userInfo.department} department
      </Typography>
      <Paper elevation={3}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="center">Name</TableCell>
              <TableCell align="center">Email</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {professors.map((professor) => (
              <TableRow key={professor.id}>
                <TableCell align="center">{professor.name}</TableCell>
                <TableCell align="center">{professor.email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Container>
  );
};

const ProtectedProfessorList = WithRole(ProfessorList, "Headmaster");

export default ProtectedProfessorList;
