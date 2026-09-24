from db_clients.base_db_client import DatabaseClient


class ProductDB(DatabaseClient):

    def get_product_by_id(self, product_id):
        return self._query("select * from products where id = %s", (product_id,))

    def get_product_price(self, product_id):
        return self._query("select price_cents from products where id = %s", (product_id,))[0][0]

    def get_product_list_count(self):
        return self._query("select count(*) from products")[0][0]