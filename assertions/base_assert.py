from requests import Response


def assert_status_code(actual: Response, expected: int):
    """
    Проверка статус кода
    :param actual: полученный статус код
    :param expected: ожидаемый статус код
    """
    assert actual.status_code == expected


def assert_equals(actual, expected):
    """
    Сравнения двух значений
    :param actual: Полученное значение
    :param expected: Ожидаемое значение
    """
    assert actual == expected


def assert_body_error_code(actual: Response, expected: int):
    """
    Проверка кода ошибки в теле ответа
    :param actual: полученный код
    :param expected: ожидаемый код
    :return:
    """
    assert actual.json()["code"] == expected


def assert_response_error_message(actual: Response, expected: str):
    """
    Проверка сообщения об ошибке в теле ответа
    :param actual: полученное сообщение об ошибке
    :param expected: ожидаемое сообщение об ошибке
    :return:
    """
    assert_equals(actual.json()["message"], expected)
