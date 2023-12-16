# Postgres Database Management Setup Script 

## Overview

The DBM setup script is a Python script designed to facilitate preparing your Postgres databses for monitoring with [Datadog's Database Monitoring](https://docs.datadoghq.com/database_monitoring/setup_postgres/selfhosted/?tab=postgres15), including user and schema creation, extension installation, and checking PostgreSQL statistics. This document provides instructions on how to use the setup script to prepare your databases. 

## Prerequisites

Before using the script, ensure the following prerequisites are met:

- Python 3.10 is installed on your system
- The database user used to connect to the Postgres instance has admin access
- Your Postgres databse has `pg_stat_statements` enabled in your `postgresql.conf` file
```
shared_preload_libraries = 'pg_stat_statements'  # (change requires restart)
```

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/dbm2.git
   cd dbm2

2. Edit the `.env`` in the project directory and add the following environment variables with your PostgreSQL connection details:
   ```
   PGHOST=your_database_host
   PGPORT=your_database_port
   PGDATABASE=your_database_name
   PGUSER=your_database_user
   PGPASSWORD=your_database_password
   DD_ROLE_NAME=datadog
   DD_ROLE_PASSWORD=datadog
   ```

3. Run the Script:
   * This command activates the virtual environment, installs/upgrades dependencies, and executes the `dbm_setup.py` script.


   ```
   make run
   ```

### Review Output:
The script will output information about the progress of tasks, such as user creation, schema creation, and PostgreSQL statistics checks.

#### Testing the script
You can test the script on a docker container to see how this works before running on your database.

To run a Postgres Docker container for testing, runt he docker command below from repo root directory:
```
docker run -d --name postgres-container -p 5446:5432 -e POSTGRES_PASSWORD=postpass -v $(pwd)/postgresql.conf:/etc/postgresql/postgresql.conf postgres -c 'config_file=/etc/postgresql/postgresql.conf'
```

To create an additional databse for testing:
```
psql -h localhost -p 5446 -U postgres -c "CREATE DATABASE testdb;"
```

![Alt text](<./img/Screen Recording 2023-11-28 at 10.11.06 AM.gif>)

### Check PostgreSQL Statistics:
After running the script, review the console output to ensure that PostgreSQL connections, activity, and statistics are reported correctly. If no errors are present, the script will print a list of databses that were successfully prepared at the end of the script.

![Alt text](<./img/Image 2023-11-28 at 11.03.44 AM.jpg>)
