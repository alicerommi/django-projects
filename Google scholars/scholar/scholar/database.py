import psycopg2
# from psycopg2 import Error
import sys


class db:
    def __init__(self):
        self.params_dic = {
            "host": "localhost",
            "database": "postgres",
            "user": "postgres",
            "password": "postgres"
        }
        self.conn = None

            # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        self.conn = psycopg2.connect(**self.params_dic)
        if self.conn:
            print("DB Connected")
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print(error)
        #     sys.exit(1)


class create_table:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_tablescholar(self):
        # try:
            table_scholar = """

            CREATE TABLE IF NOT EXISTS
            gscholar (
            id int GENERATED ALWAYS AS IDENTITY primary key,
            title text not null
            );
            """
            self.cursor.execute(table_scholar)
            self.conn.commit()
            print("Tables created successfully in PostgreSQL ")
        # except (Exception, Error) as error:
        #     print("Error while connecting to PostgreSQL", error)
        # finally:
        #     if self.conn is not None:
        #         self.conn.close()

    def delete_table_scholar(self):
        # try:
            table_scholar = """
            DROP TABLE IF EXISTS gscholar;
            """
            self.cursor.execute(table_scholar)
            self.conn.commit()
            print("Tables Deleted successfully in PostgreSQL ")
        # except (Exception, Error) as error:
        #     print("Error while connecting to PostgreSQL", error)