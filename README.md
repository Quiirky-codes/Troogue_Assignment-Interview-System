# Troogue Assignment (Interview System)

This repository contains a full-stack AI application with:
- **Backend API** built using Python (FastAPI/Flask style architecture)
- **Streamlit frontend** for an interactive UI
- **Dockerized setup** for easy local and production deployment

The entire application can be started using a single **Docker Compose** command.

---

## Project Structure

```

INTERVIEW_SYSTEM/
├── fastapi_service/
│   ├── __pycache__/
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
│
├── flask_service/
│   ├── __pycache__/
│   ├── uploads/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── models.py
│   ├── requirements.txt
│   ├── routes.py
│   ├── schemas.py
│   └── utils.py
│
├── streamlit_frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── uploads/
├── venv/
├── .env
├── .gitignore
├── docker-compose.yml
└── requirements.txt

```

---

## Tech Stack

- **Backend**: Python, FastAPI / Flask-style routing
- **Frontend**: Streamlit
- **Database**: PostgreSQL (via SQLAlchemy)
- **ORM**: SQLAlchemy
- **Containerization**: Docker & Docker Compose

---

## Running the App with Docker (Recommended)

### Prerequisites

Make sure you have:
- Docker
- Docker Compose

Check:

```

docker --version

docker compose version

```

### Clone the Repository

```

git clone https://github.com/Quiirky-codes/Troogue_Assignment-Interview-System.git

cd INTERVIEW_SYSTEM

```

### Environment Variables

Create a `.env` file in the root directory:

```

POSTGRES_USER=your_usernmae
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_databasename
POSTGRES_HOST=your_host
POSTGRES_PORT=5432

FLASK_HOST=0.0.0.0
FLASK_PORT=5001

FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

FASTAPI_URL=http://fastapi:8000

```

### Start the Application

```

docker compose up --build

```

This will:

- Build the backend service

- Start the API server

- Launch the Streamlit frontend

### Access the App


Streamlit UI: [http://localhost:8501](http://localhost:8501)


Backend API: [http://localhost:8000](http://localhost:8000)

---

## Running Locally (Without Docker)

### Create Virtual Environment

```
python -m venv venv

source venv/bin/activate  # macOS/Linux

venv\Scripts\activate     # Windows

```
### Install Dependencies

```

pip install -r requirements.txt

```

### Run Backend

```

python main.py

```
### Run Streamlit Frontend

```

streamlit run app.py

```

---

## Key Features

- Clean API-first architecture

- Interactive Streamlit UI

- Modular routing and models

- Fully Dockerized for portability

- Easy local and production deployment

---

## Future Improvements

- Authentication & authorization

- Better error handling & logging

- CI/CD pipeline

- Production-grade reverse proxy (NGINX)

---

## Project Context

This project was developed as part of a technical assignment for Troogue. The objective was to design and implement a multi-service system with a backend API, supporting services, and a Streamlit-based frontend, following real-world engineering and deployment practices.

--- 

## Application Walkthrough (Screenshots)

Below are screenshots demonstrating the complete flow of the Interview System, from candidate creation to interview completion and dashboard view.

### Create Candidate

This section shows the interface used to create a new candidate profile, which initializes the interview process.

<img width="2772" height="1674" alt="image" src="https://github.com/user-attachments/assets/9ce94d9e-536a-473b-9865-b8729a798d4c" />

**A new Candidate and Candidate ID are created.**

<img width="2844" height="1728" alt="image" src="https://github.com/user-attachments/assets/f74d1dc9-e5d4-47d8-b323-ca1bb77a41a9" />


### Create Interview

This section demonstrates how an interview is created and assigned to a candidate.

<img width="2838" height="1740" alt="image" src="https://github.com/user-attachments/assets/05fb7963-8b26-46d7-a2e8-e52bcdf0cda5" />

### Get Questions

This section displays how interview questions are fetched dynamically for the candidate.

<img width="2762" height="1736" alt="image" src="https://github.com/user-attachments/assets/163b9bcd-6eae-47d9-a30b-cfd81e988a1e" />

### Submit Answers

This section shows the interface where the candidate submits answers for the interview questions.

### Complete Interview

This section illustrates the final step where the interview is completed and submitted for evaluation.

<img width="2848" height="1804" alt="image" src="https://github.com/user-attachments/assets/39d17470-7a87-4e41-b974-bf30ed450cd9" />


### View Dashboard

This section shows the dashboard view, where interview status, results, and candidate progress can be monitored.

<img width="2836" height="1800" alt="image" src="https://github.com/user-attachments/assets/6d28a516-8956-4b62-8d02-dc592954b62f" />



