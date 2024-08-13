# Job Scheduler Microservice

## Introduction

You need to develop a scheduler microservice that allows job scheduling while maintaining critical job-related information. The service should have API endpoints for job management, such as listing all jobs, retrieving details of a specific job by ID, and creating new jobs.

## Project Structure

DIGANTARA_ASSESMENT/
│
├── app.py # Main application file containing the Flask routes and logic
├── requirements.txt # Python dependencies for the project
└── README.md # Project overview and setup instructions


## Setup Instructions

### Prerequisites

- Python 3
- MySQL database server

### Installation

1. **Clone the repository**:

    ```bash
    git clone "Use github http link here"
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your MySQL database**:

    ```sql
    CREATE TABLE jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
        time_of_day TIME NOT NULL,
        frequency VARCHAR(50) DEFAULT NULL,
        priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
        last_run DATETIME DEFAULT NULL,
        next_run DATETIME DEFAULT NULL
    );
    ```

5. **Update the database connection settings** in `config.py` and add in `app.py`.

    ```python
    def get_db_connection():
        return mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
    ```

6. **Run the application**:

    ```bash
    python app.py
    ```

7. **Access the API endpoints**:

   - List jobs: `GET http://127.0.0.1:5000/jobs`
   - Retrieve job by ID: `GET http://127.0.0.1:5000/jobs?job_id=<id>`
   - Create a job: `POST http://127.0.0.1:5000/jobs`


