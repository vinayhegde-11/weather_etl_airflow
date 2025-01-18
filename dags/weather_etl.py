# imports

from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import requests

## latitudes and longitudes of the random place
LATTITUDE = '14.49527'
LONGITUDE = '74.81805'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

## DAG
with DAG(dag_id='weather_etl_pipeline',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False) as dags:
    
    @task()
    def extract_weather_data():
        """ Extracts weather data from the Open Meteo API using Airflow Connection"""
        
        ## use http hook to get weather data through api
        # http_hook = HttpHook(http_conn_id=API_CONN_ID,method='GET')

        ## build api endpoint
        ## https://api.open-meteo.com/v1/forecast?latitude=14.49527&longitude=74.81805&current_weather=true
        endpoint = f"https://api.open-meteo.com/v1/forecast?lattitude={LATTITUDE}$longitude={LONGITUDE}&current_weather=true"

        ## make request vio http hook
        response = requests.get(endpoint, verify=False)
        if response == 200:
            return response.json()
        else:
            raise Exception(f"failed to fetch data:{response.status_code}")
        
    @task()
    def transform_weather_data(weather_data):
        """Transform extracted weather data"""
        current_weather = weather_data['current-weather']
        transformed_data = {
            'latitude': LATTITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data
    
    @task()
    def load_weather_data(transformed_data):
        """Load transformed data to Postgresql"""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        ## create table if doesnot exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data(
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        ## insert transformed data to table
        cursor.execute("""
        INSERT INTO weather_data(latitude,longitude,temperature,windspeed,winddirection,weathercode)
        VALUES(%s,%s,%s,%s,%s,%s)
        """(
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))
        conn.commit()
        cursor.close()

    ## DAG workflow
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)