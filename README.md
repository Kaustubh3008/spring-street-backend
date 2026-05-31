# Spring Street Data API

Backend infrastructure powering the Prisma factsheet experience, built for the Spring Street Engineering Internship assignment.

## 🏗 Architecture & System Design

This system is built using a modern, scalable Python stack:

- **Framework:** FastAPI (Chosen for high performance, async capabilities, and automatic OpenAPI documentation).
- **Database:** SQLite via SQLAlchemy ORM (Highly structured relational modeling for financial data, easily translatable to PostgreSQL for production).
- **ETL Pipeline:** A standalone Python script using `yfinance` to extract live market data, transform it to calculate accurate sector exposures, and load it into the database.
- **Data Freshness:** The ETL pipeline (`etl.py`) is designed as a modular job. In a production environment, this would be scheduled via a Cron job or Airflow to run daily at market close, ensuring the factsheet always displays T-1 data without slowing down user API requests.

## 🚀 Setup Instructions

Follow these steps to run the backend locally.

### 1. Environment Setup

Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
```

### 2. Install Dependencies

pip install fastapi uvicorn yfinance pandas sqlalchemy pydantic

### 3. Run the ETL Pipeline

python etl.py

### 3.Start the API Server

uvicorn main:app --reload
