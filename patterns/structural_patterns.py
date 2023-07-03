from time import time


# Структурный паттерн - Декоратор
class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        :param routes: принимает словарь, который находится в оперативной памяти и пополняемый элементами
        :param url: маршрут
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """Сам декоратор"""
        self.routes[self.url] = cls()  # В словарь кладём элемент, где url-ключ, а значение-объект класса (обработчик).


# структурный паттерн - Декоратор
class Debug:

    def __init__(self, name):
        """
        :param name: имя контроллера, какой класс замеряем
        """
        self.name = name

    def __call__(self, cls):
        """Сам декоратор"""

        def timeit(method):
            """Вспомогательная функция будет декорировать каждый отдельный метод класса
            Нужен для того, чтобы декоратор класса wrapper обернул в timeit каждый метод декорируемого класса"""
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
