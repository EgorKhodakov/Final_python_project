class DatabaseClient:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def _query(self, query, param=None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)
        return self.cursor.fetchall()