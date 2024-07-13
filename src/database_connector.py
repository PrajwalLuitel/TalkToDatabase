import re
import sqlalchemy.exc
from typing import Literal
from langchain import SQLDatabase
from sqlalchemy import create_engine


class SQLAgent:

    def __init__(
        self,
        host_name: str,
        port: int,
        username: str,
        database_name: str,
        database_type=Literal["MySQL", "PostgreSQL", "MariaDB", "SQLite", "Oracle SQL"],
        password: str = None,
    ) -> None:
        self.__host_name: str = host_name
        self.__port: int = port
        self.__username: str = username
        self.__password: str = password
        self.__db_name: str = database_name
        self.db_type: str = database_type

        # check the connection
        self.__check_connection()

    def __get_table_names_schema_re(self, engine):

        regex = r"CREATE TABLE .*?\)\n"

        schemas = re.findall(regex, engine, re.DOTALL)

        tables = re.findall(r'CREATE TABLE "?(.*?)"? \(', engine)

        return tables, schemas

    def __generate_conn_str(self):
        """
        Generates connection string based on the type of database

        """
        conn_mapp = {
            "MySQL": f"mysql+pymysql://{self.__username}:{self.__password}@{self.__host_name}:{str(self.__port)}/{self.__db_name}",
            "PostgreSQL": f"postgresql+psycopg2://{self.__username}:{self.__password}@{self.__host_name}:{str(self.__port)}/{self.__db_name}",
        }

        conn_str = conn_mapp.get(self.db_type)

        if conn_str is None:

            raise NotImplementedError(f"Not implemented for {self.db_type}.")

        else:

            return conn_str

    def exract_db_info(self):

        # step 1 : get the connection string
        connection_str = self.__generate_conn_str()

        try:
            # step 2 : Check connection to database
            db_engine = SQLDatabase.from_uri(connection_str)

            # Step 3: Grab the tables and other
            tables, schema = self.__get_table_names_schema_re(
                engine=db_engine.table_info
            )

            return tables, schema

        except sqlalchemy.exc.OperationalError as e:

            raise e

    def __check_connection(self):

        # get the connection string
        connection_str = self.__generate_conn_str()

        engine = create_engine(connection_str)

        try:
            engine.connect()
            print("Connection to MySQL database successful!")

        except Exception as e:

            raise f"Error connecting to MySQL database: {e}"
