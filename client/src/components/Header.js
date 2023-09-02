import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Header = () => {
  const { userInfo, isLoading } = useAuth();

  const roleBasedRoutes = {
    Professor: [
      { path: "/dashboard", text: "Dashboard" },
      { path: "/grades", text: "Grades" },
      { path: "/logout", text: "Logout" },
    ],
    Headmaster: [
      { path: "/dashboard", text: "Dashboard" },
      { path: "/upload-csv", text: "Upload Scores" },
      { path: "/logout", text: "Logout" },
    ],
    "QA Officer": [
      { path: "/professors", text: "Professors" },
      { path: "/reports", text: "Reports" },
      { path: "/logout", text: "Logout" },
    ],
  };

  const renderLinks = () => {
    if (isLoading) {
      return <div>Loading...</div>;
    }

    const links = userInfo
      ? roleBasedRoutes[userInfo.role]
      : [{ path: "/login", text: "Login" }];
    return links.map((link, index) => (
      <Link
        key={index}
        to={link.path}
        style={{ color: "white", textDecoration: "none", marginRight: 15 }}
      >
        {link.text}
      </Link>
    ));
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">University QA App</Typography>
        <div style={{ marginLeft: "auto" }}>
          <Link
            to="/"
            style={{ color: "white", textDecoration: "none", marginRight: 15 }}
          >
            Home
          </Link>
          {renderLinks()}
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
