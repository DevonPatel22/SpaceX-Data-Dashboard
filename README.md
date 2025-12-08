# IEE-305-Term-Project

## Team Members
- Devon Patel (dpate296)
- Joel Cabral (jecabra3)

## Description
SpaceX database to help program managers make better decisions for future projects based upon past successes and failures

## Features
- 10 SQL Queries covering
  - Launch Success/ Failure
  - Rocket Performance metrics
  - Core Reusability Tracking
  - Utilization Statistics
- RESTful API with 10 endpoints
- 3NF Normalized Database with preloaded records
- Interactive API Documentation
- Streamlit Web Based Frontend

## Technology Stack
- Backend
  - Python
  - FastAPI
  - SQLModel
  - SQLite
  - Pydantic
- Frontend
  - Streamlit
- Data Source
  - SpaceX API V4

## Installation
- Prerequisites
  - Python 3.10 or higher
  - pip
  - Git

### Step 1 : Clone the Repository
```bash
git clone https://github.com/yourusername/IEE-305-Term-Project.git
cd IEE-305-Term-Project
```

### Step 2 : Create Virtual Environment
```bash 
python -m venv venv
.\venv\Scripts\activate
```
### Step 3 : Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4 : Populate Database
```bash
cd backend
python fetch_data.py
```
- This will
  - Create the SQLite Database
  - Fetch the data from the SpaceX API
  - Populate the tables with records

## Usage 

### Start Backend 

1. Navigate to the backend directory:
```bash
cd backend
```

2. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

3. The API will be available at:
```
http://127.0.0.1:8000
```

4. View interactive API documentation:
```
http://127.0.0.1:8000/docs
```

### Start Frontend
```bash
cd frontend
streamlit run app.py
```

## API Documentation
### Endpoints:
- /launches/fails
  - Displays all failed launches
- /launches/succeeded
  - Displays all launches that succeeded
- /launches/details
  - Displays all launch details
- /launches/count
  - Displays number of launches
- /launches/countSuccess 
  - Displays Number of successful launches
- /launches/countFailed
  - Displays number of launches failed
- /rockets/highStage
  - Displays rocket information that reached the highest stage
- /rockets/stageAscending
  - Orders Rockets under stage 2 from lowest to highest stage
- /cores/reuseCount
  - Displays the number of times a core has been reused
- /launches/byRocketID
  - Displays data for specific rocket given its ID

## Database Schema 

Table 1: Launch
CREATE TABLE "Launch" (
	"ID"	TEXT,
	"rocketID"	INTEGER,
	"coreID"	INTEGER,
	"launchDate"	DATETIME,
	"flightNumber"	INTEGER,
	"launchSuccess"	BOOLEAN,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("coreID") REFERENCES "Cores"(“ID”),
	FOREIGN KEY("rocketID") REFERENCES "Rockets"("ID")
);

Table 2: Rockets
CREATE TABLE "Rockets" (
	"ID"	TEXT,
	"active"	BOOLEAN,
	"stages"	INTEGER,
	"successRate"	INTEGER,
	"costPerLaunch"	REAL,
	"diameter"	REAL,
	"mass"	REAL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);

Table 3: Cores
CREATE TABLE "Cores" (
	"ID"	TEXT,
	"block"	INTEGER,
	"status"	TEXT,
	"reuseCount"	INTEGER,
	"rtlsLandings"	INTEGER,
	"asdsLandings"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);

## Project Structure

```
IEE-305-Term-Project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── database.py          # Database connection
│   ├── fetch_data.py        # Data fetching script
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── streamlit.py         # Frontend application
├── database.db              # SQLite database
└── README.md                # This file
```
