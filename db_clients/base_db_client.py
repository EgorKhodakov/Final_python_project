class DatabaseClient:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def _query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()