from db_clients.base_db_client import DatabaseClient

class UserDB(DatabaseClient):


    def get_user_by_id(self, user_id):
        return self._query("select * from users where id = %s", (user_id,))

    def get_user_email(self, user_id):
        return self._query("select email from users where id = %s", (user_id,))
