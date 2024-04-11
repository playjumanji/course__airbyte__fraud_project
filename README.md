# Fraud Detection Project: Airflow -> Airbyte -> dbt -> SODA

## 0. Installation
All you need to do to install it locally is python3.12 and then run:
```bash
poetry install
```
After this, you can simply start the stack of containers using docker:
```bash
docker compose up -d
```
You might then get a compose stack like this:
![docker compose up](docs/images/docker_compose_up.png)


## 1. Initializing
Now that you have the containers running, you need to generate your source data. This is done by logging into airflow. To do it open in your browser ```http://localhost:8080```. 
- user: airflow
- password: airflow

Activate and run the DAG ```generate_data```.

![DAG generate_data](docs/images/airflow_dag_generate_data.png)

After running this DAG, you'll have these tables loaded in these databases:

- MYSQL
    host: 

## Configuration
### Configure the airbyte connection
- Connection id: airbyte
- Connection type: Airbyte
- Host: airbyte-server
- Port: 8001
![Airflow connection: airbyte](docs/images/airflow_connection_airbyte.png)

# The Aiflow DAG
After changing all the necessary variables in the project, you can log into airflow and check this DAG availabe in your DAG list:
![DAG list](docs/images/airflow_dag_list.png)

The you can select this one and check the details:
![DAG customer_metrics](docs/images/airflow_dag_customer_metrics.png)