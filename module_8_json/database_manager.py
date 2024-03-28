import pyodbc


class DatabaseManager:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQLite3 ODBC Driver};'
                            'Direct=True;'
                            'Database=target_database.db;'
                            'Trusted_connection=yes'
                            , autocommit=True
                            )
        self.cur = self.conn.cursor()

    def create_tables(self):
        queries = ["CREATE TABLE IF NOT EXISTS news (id integer PRIMARY KEY, text text NOT NULL, city text NOT NULL);",
                   "CREATE TABLE IF NOT EXISTS ad (id integer PRIMARY KEY, text text NOT NULL, exp_date text NOT NULL);",
                   "CREATE TABLE IF NOT EXISTS song (id integer PRIMARY KEY, text text NOT NULL);"]

        for query in queries:
            self.cur.execute(query)

    def check_duplicate_and_insert(self, table, **params):
        condition = ' and '.join([f"{key} = '{value}'" for key, value in params.items()])
        self.cur.execute(f"SELECT * FROM {table} WHERE {condition}")

        if not self.cur.fetchall():
            columns = ', '.join([key for key in params.keys()])
            values = ', '.join([f"'{value}'" for value in params.values()])
            self.cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        else:
            print(f"Record already exists in the {table} table. Skipping...")
