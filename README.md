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
