import psycopg2

class ConnectionDB:
    def __init__(self, host='localhost', database='pythonconn', username='postgres', pwd='passw54321', port_id=5432):
        self.connection = psycopg2.connect(dbname=database, user=username, password=pwd)
        self.cursor = self.connection.cursor()


    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

