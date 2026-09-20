from db_clients.database_facade import FacadeDB


def test_get_user_from_db( data_base: FacadeDB):
    print(data_base.users.get_user_email("0b69cba9-1f05-4b46-8f86-dcb343813efd")[0][0])










