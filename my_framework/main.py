# Центр управления фреймворком =)

from quopri import decodestring
from my_framework.my_requests import GetRequests, PostRequests


class PageNotFound404:
    """Если пришёл запрос на не существующий контроллер - возвращаем ответ
    с кодом 404 ошибки и телом ответа"""

    def __call__(self, request):
        return '404 WHAT', 'Error 404. Page not found'


class MyFramework:
    """
    Главный класс фреймворка.
    При инициализации получает списки контроллеров "routes" и фронтов "fronts"
    для изменения обработки всех запросов без изменения фреймворка.
    """

    def __init__(self, routes, fronts):
        self.routes_lst = routes
        self.fronts_lst = fronts

    def __call__(self, environ, start_response):
        # Делаем перегрузку вызова, чтобы вызывать объект класса.
        # Получаем адрес запроса для перехода по ссылке.
        path = environ['PATH_INFO']

        # Добавляем закрывающий / в запрос урла, если его не было.
        if not path.endswith('/'):
            path = f'{path}/'

        # Реализация Front controller - создаём словарь действий, для всех контроллеров.
        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']  # по ключу
        print(f'method: {method}')
        request['method'] = method

        # В зависимости от полученного метода выполняем POST или GET
        # Если метод POST:
        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = MyFramework.decode_value(data)
            print(f'POST-запрос: {MyFramework.decode_value(data)}')
        # Если метод GET:
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = MyFramework.decode_value(request_params)
            print(f'GET-параметры: {MyFramework.decode_value(request_params)}')

        # Реализация Page controller
        # Проверяем полученный адрес запроса на нужный контроллер.
        if path in self.routes_lst:
            view = self.routes_lst[path]

        # Если таковой отсутствует присваиваем 404 ошибку:
        else:
            view = PageNotFound404()

        # Заполняем словарь request.
        for front in self.fronts_lst:
            front(request)

        # Выводим в консоль терминала, показать работоспособность
        print(f'request: {request}')

        # Присваиваем значения кода ответа и тела ответа, передавая объекта request
        code, body = view(request)

        # Запускаем контроллер
        start_response(code, [('Content-Type', 'text/html')])

        # Возвращаем в закодированном виде
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """
        Декодирует данные
        :param data:
        :return: -> dict
        """
        print(f'тут будут data: {data}')
        new_data = {}
        for k, v in data.items():
            # Меняем значения разделителей
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            # Декодируем
            val_decode_str = decodestring(val).decode('UTF-8')
            # Наполняем словарь
            new_data[k] = val_decode_str
        return new_data
