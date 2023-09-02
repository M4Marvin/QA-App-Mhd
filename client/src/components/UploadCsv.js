import React, { useState, useEffect } from "react";
import {
  Button,
  Container,
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import Papa from "papaparse";
import * as XLSX from "xlsx";
import WithRole from "./WithRole";
import { uploadFile } from "../api/api";
// import reader

const UploadCSV = () => {
  const [fileData, setFileData] = useState(null);
  const [file, setFile] = useState(null); // new state for file
  const [error, setError] = useState(null); // new state for error messages

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile); // set file to state

    if (!selectedFile) {
      console.log("No file selected.");
      return;
    }

    const reader = new FileReader();

    reader.onload = (evt) => {
      if (selectedFile.type === "text/csv") {
        Papa.parse(evt.target.result, {
          header: true,
          dynamicTyping: true,
          complete: function (result) {
            setFileData(result.data);
          },
        });
      } else if (selectedFile.type.includes("spreadsheetml")) {
        const workbook = XLSX.read(evt.target.result, { type: "binary" });
        const sheetname = workbook.SheetNames[0];
        const ws = workbook.Sheets[sheetname];
        const data = XLSX.utils.sheet_to_json(ws);
        setFileData(data);
      }
    };

    if (selectedFile.type === "text/csv") {
      reader.readAsText(selectedFile);
    } else {
      reader.readAsBinaryString(selectedFile);
    }
  };

  const handleConfirmUpload = async () => {
    if (!fileData || !file) {
      setError("No file or file data to upload.");
      return;
    }

    try {
      const uploadResponse = await uploadFile(file);
      console.log("Upload successful:", uploadResponse);
      setError(null); // Clear error on successful upload
    } catch (error) {
      console.error("Upload failed:", error);
      setError(error.message); // Set the error message
    }
  };

  return (
    <Container maxWidth="md">
      <Box mt={4}>
        <Typography variant="h4" mb={4}>
          Upload CSV/Excel File
        </Typography>
        <input
          accept=".csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          style={{ display: "none" }}
          id="upload-file"
          type="file"
          onChange={handleFileUpload}
        />
        <label htmlFor="upload-file">
          <Button variant="contained" color="primary" component="span">
            Upload File
          </Button>
        </label>
        {fileData && (
          <Box mt={4}>
            <Typography variant="h6" mb={2}>
              Preview Data
            </Typography>
            <Table>
              <TableHead>
                <TableRow>
                  {Object.keys(fileData[0]).map((key, index) => (
                    <TableCell key={index}>{key}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {fileData.map((row, index) => (
                  <TableRow key={index}>
                    {Object.values(row).map((value, idx) => (
                      <TableCell key={idx}>{value}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <Box mt={4}>
              <Button
                variant="contained"
                color="secondary"
                onClick={handleConfirmUpload}
              >
                Confirm Upload
              </Button>
            </Box>
            {error && (
              <Box mt={4}>
                <Typography variant="body1" color="error">
                  {error}
                </Typography>
              </Box>
            )}
          </Box>
        )}
      </Box>
    </Container>
  );
};

const HeadmasterUploadCSV = WithRole(UploadCSV, ["Headmaster"]);

export default HeadmasterUploadCSV;
