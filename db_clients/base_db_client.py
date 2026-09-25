class DatabaseClient:
    def __init__(self, connection):
        self.connection = connection

    def _query(self, query, param=None):
        with self.connection.cursor() as cursor:
            if param is not None:
                cursor.execute(query, param)
            else:
                cursor.execute(query)
            if cursor.description:
                return cursor.fetchall()
            else:
                return cursor.rowcount
