#!/bin/bash
export PROJECT_ROOT_DIR=$(pwd)

export DBT_PROFILES_DIR="${PROJECT_ROOT_DIR}/include/dbt/fraud"
export DBT_PROJECT_DIR=${DBT_PROFILES_DIR}

cd include/dbt
poetry run dbt debug
poetry run dbt compile
poetry run dbt run
