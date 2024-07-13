import re
import pandas as pd
from sqlalchemy import create_engine, text


class SQLExtractor:
    def __init__(self, text: str):
        self.text = text

    def extract_select_commands(self):
        # Regular expression to find all SELECT commands
        select_pattern = re.compile(r"SELECT\s.*?;", re.IGNORECASE | re.DOTALL)
        select_commands = select_pattern.findall(self.text)
        return select_commands


def get_data_from_query(query, db_url, params=None):
    engine = create_engine(db_url)
    query = text(query)
    with engine.connect() as connection:
        raw_conn = connection.connection
        data = pd.read_sql_query(str(query), raw_conn, params=params)
    engine.dispose()
    return data
