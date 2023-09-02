// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import Login from "./components/Login";
import ProtectedProfessorList from "./components/ProfessorList";
import Home from "./components/Home";
import Header from "./components/Header";
import AccessDenied from "./components/AccessDenied";
import HeadmasterUploadCSV from "./components/UploadCsv";
import Logout from "./components/Logout";
import ProtectedGrades from "./components/Grades";

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/professors" element={<ProtectedProfessorList />} />
          <Route path="/upload-csv" element={<HeadmasterUploadCSV />} />
          <Route path="/grades" element={<ProtectedGrades />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/access-denied" element={<AccessDenied />} />
          <Route path="*" element={<h1>Not Found</h1>} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
