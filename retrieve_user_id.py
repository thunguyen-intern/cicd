from json import dumps
from sys import argv
from httplib2 import Http
import env_db_vars
import psycopg2

if __name__ == "__main__":
    id = "all"
    db_host = env_db_vars.DB_HOST
    db_name = env_db_vars.DB_NAME
    db_user = env_db_vars.DB_USER
    db_password = env_db_vars.DB_PASSWORD
    db_table = env_db_vars.DB_TABLE
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        select_query = "SELECT * FROM {} WHERE email='{}';".format(db_table, argv[1])
        cursor.execute(select_query, (argv[1]))
        connection.commit()
        res = cursor.fetchall()
        print(res[0][1].strip())
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)