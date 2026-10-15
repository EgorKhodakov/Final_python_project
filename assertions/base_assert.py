from typing import Any, Sized

from httpx import Response


def assert_status_code(actual: Response, expected: int):
    """
    Проверка статус кода
    :param actual: полученный статус код
    :param expected: ожидаемый статус код
    """
    assert actual.status_code == expected


def assert_equals(actual: Any, expected: Any):
    """
    Сравнения двух значений
    :param actual: Полученное значение
    :param expected: Ожидаемое значение
    """
    assert actual == expected


def assert_len(actual: Sized, expected: int):
    """
    Сравнение длинны объекта
    :param actual: получаемый объект
    :param expected: ожидаемое значение
    """
    assert len(actual) == expected


def assert_is_true(actual: Any):
    """
    Проверка истинности утверждения
    :param actual: получаемый объект
    """
    assert actual


def assert_body_error_code(actual: Response, expected: int):
    """
    Проверка кода ошибки в теле ответа
    :param actual: полученный код
    :param expected: ожидаемый код
    """
    assert actual.json()["code"] == expected


def assert_response_error_message(actual: Response, expected: str):
    """
    Проверка сообщения об ошибке в теле ответа
    :param actual: полученное сообщение об ошибке
    :param expected: ожидаемое сообщение об ошибке
    """
    assert_equals(actual.json()["message"], expected)
