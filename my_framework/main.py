# Центр управления фреймворком =)

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

        # Реализация Page controller
        # Проверяем полученный адрес запроса на нужный контроллер.
        if path in self.routes_lst:
            view = self.routes_lst[path]

        # Если таковой отсутствует присваиваем 404 ошибку:
        else:
            view = PageNotFound404()

        # Реализация Front controller - создаём словарь действий, для всех контроллеров.
        request = {}

        # Заполняем словарь
        for front in self.fronts_lst:
            front(request)

        # Выводим в консоль терминала, показать работоспособность
        print(request)

        # Присваиваем значения кода ответа и тела ответа, передавая объекта request
        code, body = view(request)

        # Запускаем контроллер
        start_response(code, [('Content-Type', 'text/html')])

        # Возвращаем в закодированном виде
        return [body.encode('utf-8')]
