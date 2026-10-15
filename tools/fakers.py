from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker, который будет использоваться для генерации данных.
        """
        self.faker = faker

    def text(self) -> str:
        """
        Генерирует случайный текст
        :return: Случайный текст
        """
        return self.faker.text()

    def uid(self) -> str:
        """
        Генерирует случайный UID
        :return: случайный UID
        """
        return self.faker.uuid4()

    def email(self, domain: str | None = None) -> str:
        """
        Генерирует случайный email
        :param domain: домен электронной почты
        :return: случайный email
        """
        return self.faker.email(domain=domain)

    def password(self) -> str:
        """
        Генерирует случайный пароль
        :return:случайный пароль
        """
        return self.faker.password()

    def last_name(self) -> str:
        """
        Генерирует случайную фамилию.
        :return:Случайная фамилия.
        """
        return self.faker.last_name()

    def first_name(self) -> str:
        """
        Генерирует случайное имя.
        :return:Случайное имя.
        """
        return self.faker.first_name()

    def middle_name(self) -> str:
        """
        Генерирует случайное отчество/среднее имя.
        :return:Случайное отчество.
        """
        return self.faker.first_name()

    def integer(self, start: int = 1, end: int = 100):
        """
        Генерирует случайное целое число в заданном диапазоне.
        :param start: Начало диапазона (включительно)
        :param end: Конец диапазона (включительно)
        :return: Случайное целое число
        """
        return self.faker.random_int(start, end)


fake = Fake(faker=Faker())
