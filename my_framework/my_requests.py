# Мои запросы

class GetRequests:
    """Запрос GET"""

    @staticmethod
    def parse_input_data(data: str):
        """
        Парсит входящие данные: разделяет сначала по символу &, затем на пары ключ и значение по символу =
        :param data: входящие данные -> str
        :return: dict
        """
        result = {}  # Пустой словарь, который будет наполнен в результате
        if data:
            # Разделяем параметры через "&"
            params = data.split('&')
            for item in params:
                # Разделяем ключ и значение через "="
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        """
        Получает параметры запроса и возвращает в виде словаря
        :param environ: параметры запроса -> str
        :return: dict
        """
        # Получаем параметры запроса по ключу
        query_string = environ['QUERY_STRING']
        # Преобразуем параметры запроса в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests:
    """Запрос POST"""

    @staticmethod
    def parse_input_data(data: str):
        """
        Парсит входящие данные: разделяет сначала по символу &, затем на пары ключ и значение по символу =
        :param data: входящие данные -> str
        :return: dict
        """
        result = {}  # Пустой словарь, который будет наполнен в результате
        if data:
            # Разделяем параметры через "&"
            params = data.split('&')
            for item in params:
                # Разделяем ключ и значение через "="
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """
        Получает запрос, проверяет его длину, если она больше 0, то запускает режим чтения.
        Возвращает в байтах значение или пусто.
        :param env: запрос
        :return: -> bytes
        """
        # Получаем из запроса длину
        content_length_data = env.get('CONTENT_LENGTH')
        # Приводим к числовому значению, если оно есть, если нет присваиваем 0
        content_length = int(content_length_data) if content_length_data else 0
        print(f'content_length: {content_length}')

        # При наличии данных запускаем режим чтения
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """
        Декодирует данные, парсит из и собирает в словарь
        :param data: Данные в байтах
        :return: -> dict
        """
        result = {}  # Пустой словарь, который будет наполнен в результате
        if data:
            # Декодируем полученные данные
            data_str = data.decode(encoding='utf-8')
            print(f'Декодировали данные в строку: {data_str}')
            # Наполняем данные в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        """
        Получает данные запроса, переводит в словарь
        :param environ: параметры запроса
        :return: -> dict
        """
        # Получаем данные запроса
        data = self.get_wsgi_input_data(environ)
        # Переводим данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data
