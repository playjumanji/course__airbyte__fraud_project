import logging
from datetime import datetime

from airflow.decorators import task, dag
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig
from include.dbt.fraud.cosmos_config import DBT_CONFIG, DBT_PROJECT_CONFIG

AIRBYTE_JOB_ID_LOAD_CUSTOMER_TRANSACTIONS_RAW="378bfd74-100d-4832-9e27-06849ef789ba"
AIRBYTE_JOB_ID_LOAD_LABELED_TRANSACTIONS_RAW="cc40fe0f-9d3b-4c8f-a693-da9963ee5c34"
VENV_PATH_SODA="/opt/airflow/soda_venv/bin/python"

@dag(
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['stack:airbyte', 'analysis:risk', 'layer:silver'],
)
def customer_metrics():
    
    load_customer_transactions_raw = AirbyteTriggerSyncOperator(
        task_id="load_customer_transactions_raw",
        airbyte_conn_id="airbyte",
        connection_id=AIRBYTE_JOB_ID_LOAD_CUSTOMER_TRANSACTIONS_RAW,
    )


    load_labeled_transactions_raw = AirbyteTriggerSyncOperator(
        task_id="load_labeled_transactions_raw",
        airbyte_conn_id="airbyte",
        connection_id=AIRBYTE_JOB_ID_LOAD_LABELED_TRANSACTIONS_RAW,
    )


    @task
    def airbyte_jobs_done() -> bool:
        logging.info("Airbyte data load done!")
        return True


    @task.external_python(VENV_PATH_SODA)
    def audit__bronze__raw__postgres(
        scan_name="bronze__raw__postgres",
        checks_subpath="bronze/raw__postgres",
        data_source="raw__postgres",
    ):
        from include.soda.helpers import check
        check(scan_name, checks_subpath, data_source)
        
    
    @task.external_python(VENV_PATH_SODA)
    def audit_bronze__raw__mysql(
        scan_name="bronze__raw__mysql",
        checks_subpath="bronze/raw__mysql",
        data_source="raw__mysql",
    ):
        from include.soda.helpers import check
        check(scan_name, checks_subpath, data_source)


    @task
    def soda_quality_checks_done() -> bool:
        logging.info("SODA checks done!")
        return True


    publish = DbtTaskGroup(
        group_id="publish",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=["path:models"],
        )
    )

    # Taskflow
    (
        [load_customer_transactions_raw, load_labeled_transactions_raw] 
        >> airbyte_jobs_done()
        >> [audit__bronze__raw__postgres(), audit_bronze__raw__mysql()] 
        >> soda_quality_checks_done()
        >> publish
    )

customer_metrics()