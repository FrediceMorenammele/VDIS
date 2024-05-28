import psycopg2
from datetime import datetime

class PostgreTableManager:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to the PostgreSQL database")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def create_table(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS your_table (
                id SERIAL PRIMARY KEY,
                count INTEGER,
                insert_time TIMESTAMP
            )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while creating table:", error)


    def insert_data(self, count):
        try:
            insert_query = '''
            INSERT INTO your_table (count, insert_time)
            VALUES (%s, %s)
            '''
            timestamp = datetime.now()
            data = (count, timestamp)
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data:", error)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection closed")

# Usage example
table_manager = PostgreTableManager(
    username="your_username",
    password="your_password",
    host="your_host",
    port="your_port",
    database="your_database"
)
table_manager.connect()
table_manager.create_table()

# Your logic to count vehicles
count = 5  # Example count value
table_manager.insert_data(count)

table_manager.close_connection()
