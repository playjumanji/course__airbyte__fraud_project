#!/bin/bash

# raw_postgres
source .env

poetry run soda test-connection -d raw__postgres -c include/soda/configuration.yml -V
poetry run soda scan -v -l -d raw__postgres -c include/soda/configuration.yml include/soda/checks/tables/bronze/raw__postgres/customer_transactions.yml

poetry run soda test-connection -d raw__mysql -c include/soda/configuration.yml -V
poetry run soda scan -v -l -d raw__mysql -c include/soda/configuration.yml include/soda/checks/tables/bronze/raw__mysql/labeled_transactions.yml
