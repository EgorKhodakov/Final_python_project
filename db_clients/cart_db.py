from tkinter.constants import BROWSE

from db_clients.base_db_client import DatabaseClient


class CartDB(DatabaseClient):

    def get_cart(self, user_id):
        return self._query("select * from carts where user_id = %s", [user_id])

    def get_product_id_from_cart(self, user_id):
        rows = self._query(
            "select product_id from cart_items where user_id = %s", [user_id]
        )
        return [row[0] for row in rows]
