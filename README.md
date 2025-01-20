# dataengineering_openweathermapAPI_airflow

This project is an Airflow Directed Acyclic Graph (DAG) designed to extract weather data from an external API, transform the data, and load it into a destination system. The pipeline performs the following steps:

    Check API Availability: Ensure the weather API is available using HttpSensor.
    Extract Weather Data: Fetch the weather data from the external API using HttpOperator.
    Transform and Load Data: Perform transformations on the weather data and load it into a desired destination using a custom Python function.

Data Flow

The tasks are connected in a linear sequence:

    is_weather_api_ready → 2. extract_weather_data → 3. transform_load_weather_data

This means that:

    The extract_weather_data task will only run if the is_weather_api_ready task succeeds.
    The transform_load_weather_data task will only run if extract_weather_data succeeds.
Configuration
API Connection Configuration

To interact with the weather API, you will need to set up an Airflow connection in the Airflow UI:

    Go to the Airflow UI (typically running on http://localhost:8080).
    Navigate to Admin → Connections.
    Create a new HTTP connection with the following settings:
        Conn ID: weathermap_api
        Conn Type: HTTP
        Host: https://api.openweathermap.org
        Schema: https
        Login: (your API key if needed)

Make sure to replace the API key in the endpoint URL or set it as a secret in your Airflow environment.
Transform and Load Function

The transform_load_data function should be defined in the pipelines/transform_load_data.py file. This function is responsible for processing and loading the extracted weather data.
