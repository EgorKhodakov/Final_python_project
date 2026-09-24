from db_clients.database_facade import FacadeDB


def test_get_product_list_count( data_base: FacadeDB):
    print(data_base.products.get_product_list_count())










