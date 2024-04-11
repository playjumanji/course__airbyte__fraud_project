-- set variables (these need to be uppercase)
set airbyte_role = 'AIRBYTE_ROLE';
set airbyte_username = 'AIRBYTE_USER';
set airbyte_warehouse = 'AIRBYTE_WAREHOUSE';
set airbyte_database = 'PROJECT';
set schema_postgres = 'RAW__POSTGRES';
set schema_mysql = 'RAW__MYSQL';


create database if not exists identifier($airbyte_database);
commit;

-- grant Airbyte warehouse access
grant USAGE
on warehouse identifier($airbyte_warehouse)
to role identifier($airbyte_role);

-- grant Airbyte database access
grant OWNERSHIP
on database identifier($airbyte_database)
to role identifier($airbyte_role);

commit;

begin;

USE DATABASE identifier($airbyte_database);

-- create schema for Airbyte data
CREATE SCHEMA IF NOT EXISTS identifier($schema_postgres);
CREATE SCHEMA IF NOT EXISTS identifier($schema_mysql);

commit;

begin;

-- grant Airbyte schema access
grant OWNERSHIP
on schema identifier($schema_postgres)
to role identifier($airbyte_role);

grant OWNERSHIP
on schema identifier($schema_mysql)
to role identifier($airbyte_role);


commit;