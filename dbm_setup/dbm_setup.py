import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

GREEN = "\033[0;32m"
RED = "\033[0;31m"
RESET = "\033[0m"
DD_ROLE_PASSWORD = os.getenv('DD_ROLE_PASSWORD')
DD_ROLE_NAME = os.getenv('DD_ROLE_NAME')


def print_error(message):
    print(f"{RED}{message}{RESET}")

def print_success(message):
    print(f"{GREEN}{message}{RESET}")

def get_connection_params():
    return {
        'host': os.getenv('PGHOST'),
        'port': os.getenv('PGPORT'),
        'dbname ': os.getenv('PGDATABASE '),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('PGPASSWORD')
    }

def get_version(conn):
    try:
        with conn.cursor() as cur:
            #version2 = cur.execute("SELECT VERSION();")
            cur.execute("SHOW SERVER_VERSION;")
            version = float(str(cur.fetchone()[0].split(' ')[0])[0:3])
    except psycopg2.Error as exc:
        print(f"Error determining version: {exc}")
    return version


def create_datadog_user_and_schema(conn, db, version):
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{DD_ROLE_NAME}'")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE USER {DD_ROLE_NAME} WITH PASSWORD '{DD_ROLE_PASSWORD}'")
                print_success(f"{DD_ROLE_NAME} user created in {db} database")
                conn.commit()

        with conn.cursor() as cur:
            cur.execute(f"SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{DD_ROLE_NAME}')")
            schema_exists = cur.fetchone()[0]
    except Exception as exc:
        print_error(f"An error occurred while querying for schema {exc}")

    if schema_exists:
        print_error(f"datadog schema already exists in {db} database")

    try:
        with conn.cursor() as cur:
            print(f"Preparing postgres version {version}")
            if version >= 15:
                cur.execute(f"ALTER ROLE {DD_ROLE_NAME} INHERIT;")
                cur.execute(f"CREATE SCHEMA datadog; GRANT USAGE ON SCHEMA datadog TO {DD_ROLE_NAME}; GRANT USAGE ON SCHEMA public TO {DD_ROLE_NAME}; GRANT pg_monitor TO {DD_ROLE_NAME};")
            elif version < 15 and version >= 10:
                cur.execute(f"CREATE SCHEMA datadog; GRANT USAGE ON SCHEMA datadog TO {DD_ROLE_NAME}; GRANT USAGE ON SCHEMA public TO {DD_ROLE_NAME}; GRANT pg_monitor TO {DD_ROLE_NAME};")
            elif version < 10:
                cur.execute(f"CREATE SCHEMA datadog; GRANT USAGE ON SCHEMA datadog TO {DD_ROLE_NAME}; GRANT USAGE ON SCHEMA public TO {DD_ROLE_NAME}; GRANT SELECT ON pg_stat_database TO {DD_ROLE_NAME}; CREATE EXTENSION IF NOT EXISTS pg_stat_statements;")
            
            print_success(f"datadog schema created and permissions granted in {db} database")
            conn.commit()
    except Exception as e:
        print_error(f"An error occurred while creating datadog schema and granting permissions: {e}")

def explain_statement(conn, version):
    if version >= 15:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE OR REPLACE FUNCTION datadog.explain_statement(
                    l_query TEXT,
                    OUT explain JSON
                )
                RETURNS SETOF JSON AS
                $$
                DECLARE
                    curs REFCURSOR;
                    plan JSON;
                BEGIN
                    OPEN curs FOR EXECUTE pg_catalog.concat('EXPLAIN (FORMAT JSON) ', l_query);
                    FETCH curs INTO plan;
                    CLOSE curs;
                    RETURN QUERY SELECT plan;
                END;
                $$
                LANGUAGE 'plpgsql'
                RETURNS NULL ON NULL INPUT
                SECURITY DEFINER;
                """)
                conn.commit()
            print_success("Explain plans statement completed")
        except Exception as exc:
            print_error(f"Error encountered creating explain statement: {exc}")
    elif version < 10:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE OR REPLACE FUNCTION datadog.pg_stat_activity() RETURNS SETOF pg_stat_activity AS
                  $$ SELECT * FROM pg_catalog.pg_stat_activity; $$
                LANGUAGE sql
                SECURITY DEFINER;
                CREATE OR REPLACE FUNCTION datadog.pg_stat_statements() RETURNS SETOF pg_stat_statements AS
                    $$ SELECT * FROM pg_stat_statements; $$
                LANGUAGE sql
                SECURITY DEFINER;
                """)
                conn.commit()
            print_success("Explain plans statement completed")
        except Exception as exc:
            print_error(f"Error encountered creating explain statement: {exc}")


def create_pg_stat_statements_extension(conn_obj):
    try:
        with conn_obj.cursor() as cur:
            # Check if pg_stat_statements is already installed
            cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements';")
            result = cur.fetchone()

            if not result:
                # If not installed, then install the extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements;")
                conn.commit()
                print(f"{GREEN}pg_stat_statements extension installed successfully")
            else:
                print(f"{GREEN}pg_stat_statements extension already installed")
    except psycopg2.Error as e:
        print(f"{RED}Error installing pg_stat_statements extension: {e}")

successful_setup = []

def check_postgres_stats(conn_obj, db):
    try:
        # Create pg_stat_statements extension if not already created
        create_pg_stat_statements_extension(conn_obj)

        with conn_obj.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_stat_database LIMIT 1;")
            print(f"{GREEN}Postgres connection - OK in {db}")

            cur.execute("SELECT 1 FROM pg_stat_activity LIMIT 1;")
            print(f"{GREEN}Postgres pg_stat_activity read OK in {db}")

            cur.execute("SELECT 1 FROM pg_stat_statements LIMIT 1;")
            print(f"{GREEN}Postgres pg_stat_statements read OK in {db}")
        successful_setup.append(db_name)
        print(f"{RED}\n############### Moving On... to next database ###############################\n{RESET}")
        
    except psycopg2.OperationalError as exc:
        print(f"{RED}Error querying pg_stats from{db}{RESET}: {exc}")
    except psycopg2.Error:
        print(f"{RED}Error while accessing Postgres statistics in {db}{RESET}")

def list_databases(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
            databases = [row[0] for row in cur.fetchall() if not row[0].startswith('template')]
    except Exception as exc:
        print_error(f"Error encountered listing databases: {exc}")

    return databases

def connect_gather_db():
    try:
        connection_params = get_connection_params()
        conn = psycopg2.connect(**connection_params)
        pg_version = get_version(conn)
        databases_list = list_databases(conn)
    except psycopg2.Error as e:
        print_error(f"An error occurred while connecting to the database: {e}")
        return {}
    return pg_version, databases_list, connection_params

if __name__ == "__main__":
    pg_version, databases_list, connection_params = connect_gather_db()
    # Iterate through the list of database names, run checks, and create schemas
    for db_name in databases_list:
        print_success(f"Discovered database: {db_name}\nCreating schema and checking permissions + stats")
        connection_params['dbname'] = db_name
        conn = psycopg2.connect(**connection_params)
        create_datadog_user_and_schema(conn, db_name, pg_version)
        explain_statement(conn, pg_version)
        check_postgres_stats(conn, db_name)


print("Setup complete!")
print_success("The databse monitoring setup completed sucessfully on the following databses:")
print(f"\n {successful_setup}")