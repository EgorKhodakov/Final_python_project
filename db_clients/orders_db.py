from db_clients.base_db_client import DatabaseClient


class OrdersDB(DatabaseClient):

    def get_order_id(self, user_id):
        orders = self._query("select id from orders where user_id = %s", [user_id])
        return [order[0] for order in orders]

    def get_total_amount_cents(self, user_id):
        orders = self._query("select total_amount_cents from orders where user_id = %s", [user_id])
        return [orders[0] for order in orders]

    def get_order_status(self, user_id):
        return self._query("select status from orders where user_id = %s", [user_id])[0][0]
