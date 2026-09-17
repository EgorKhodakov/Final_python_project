from db_clients.cart_db import CartDB
from db_clients.users_db import UserDB
from db_clients.product_db import ProductDB



class FacadeDB:
    def __init__(self, connection):
        #self.orders = OrdersDB(connection)
        self.products = ProductDB(connection)
        self.users = UserDB(connection)
        self.cart = CartDB(connection)