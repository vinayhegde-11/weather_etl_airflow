# weather_etl_airflow

This project demonstrates an ETL (Extract, Transform, Load) pipeline built using Apache Airflow. The pipeline extracts weather data from the Open-Meteo API, processes it, and stores the transformed data in a PostgreSQL database.

---

## Project Structure

```
├── docker-compose.yml          # Docker Compose file for setting up PostgreSQL
├── requirements.txt            # Python dependencies for Airflow and DAGs
├── weather_etl.py              # Airflow DAG file for the ETL process
```

---

## Features
- **Data Extraction:** Fetches weather data from the Open-Meteo API.
- **Data Transformation:** Cleans and processes raw API data.
- **Data Loading:** Stores processed data in PostgreSQL.
- **Automation:** Orchestrated using Apache Airflow.

---

## Prerequisites
1. Docker and Docker Compose installed.
2. Python 3.7+ installed for local development (optional).
3. Basic knowledge of Airflow and PostgreSQL.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/vinayhegde-11/weather_etl_airflow.git
cd weather_etl_airflow
```

### 2. Install Dependencies
- If running locally:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Set Up Docker Containers
- Start PostgreSQL using Docker Compose:
  ```bash
  docker-compose up -d
  ```

### 4. Configure Airflow
1. Copy the `weather_etl.py` file to the Airflow DAGs folder:
   ```bash
   cp weather_etl.py <path-to-airflow-dags-folder>
   ```
2. Start Airflow in standalone mode:
   ```bash
   airflow standalone
   ```

### 5. Set Up Airflow Connections
- **Open-Meteo API Connection:**
  1. Navigate to Airflow UI.
  2. Go to **Admin > Connections**.
  3. Create a new connection:
     - **Connection ID:** `open_meteo_api`
     - **Connection Type:** HTTP
     - **Host:** `www.api.open-meteo.com`

- **PostgreSQL Connection:**
  1. Navigate to Airflow UI.
  2. Go to **Admin > Connections**.
  3. Create a new connection:
     - **Connection ID:** `postgres_default`
     - **Connection Type:** Postgres
     - **Host:** `postgres`
     - **Database:** `postgres`
     - **Login:** `postgres`
     - **Password:** `postgres`

### 6. Run the DAG
1. Go to the **DAGs** section in the Airflow UI.
2. Trigger the `weather_etl` DAG.

---

## File Details

### 1. `docker-compose.yml`
Configures PostgreSQL as the database service for the pipeline.

### 2. `requirements.txt`
Lists Python dependencies for the project. Install these to ensure compatibility.

### 3. `weather_etl.py`
Defines the Airflow DAG for the ETL pipeline. The DAG contains tasks for:
- Extracting data from Open-Meteo API.
- Transforming the data into a structured format.
- Loading the data into PostgreSQL.

---

## Author
Reference video: [YouTube - Airflow ETL Example](https://youtu.be/Y_vQyMljDsE?si=iSo6sQezG74UDf8M)