# Flask-React Project

## Overview

This project is a full-stack web application built with Flask and React. It allows users to upload CSV/Excel files containing professors' scores and then displays the scores in a dashboard. The application is role-based and supports different types of users, including "Headmaster" and "Professor" and "QA Officer". The headmaster can upload files and view all the data, while the professor can only view their own data. The QA officer can view all the data and can also download the data as a CSV file.

### Features

- **Secure Authentication**: Utilizes JWT for secure token-based authentication.
- **File Upload**: Supports CSV and Excel file uploads.
- **Role-based Access**: Access to different routes and data based on user role.
- **Data Visualization**: Displays uploaded data in a table.

## Technology Stack

- **Backend**: Flask
- **Frontend**: React with Material UI
- **Database**: Your_DB_Here
- **Authentication**: JWT

## Prerequisites

- Node.js and npm installed
- Python 3.x installed
- Virtual environment (Recommended)

## Installation

### Clone the Repository

```bash
git clone https://github.com/your_username/your_project_name.git
```

### Backend Setup

1. Navigate to the backend directory.

   ```bash
   cd server
   ```

2. Create a virtual environment.

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment.

   ```bash
   source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
   ```

4. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask app.

   ```bash
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend directory.

   ```bash
   cd client
   ```

2. Install the dependencies.

   ```bash
   npm install
   ```

3. Run the React app.

   ```bash
   npm start
   ```

## Usage

1. Visit `http://localhost:3000` in your web browser.
2. Log in as a headmaster or professor.
3. Use the upload button to upload a CSV or Excel file containing the professors' scores.
4. View the uploaded data on the dashboard.

## API Documentation

**Base URL**: `http://localhost:5000/`

- `/upload-scores-csv` (POST)
  - Uploads a CSV file containing scores.
- `/get-scores` (GET)
  - Retrieves the scores for the logged-in professor.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
