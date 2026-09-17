from db_clients.base_db_client import DatabaseClient


class UserDB(DatabaseClient):


    def get_user(self):
        return self._query("select * from users")





