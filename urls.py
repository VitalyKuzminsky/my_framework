from datetime import date
from views import Index, Contact


# Реализация Front controller
def front_1(request):
    request['Пасхалка_1'] = 'Hello World!'


def front_2(request):
    request['Пасхалка_2'] = 'Все запросы работают с Front controller'


# Список фронтов для всех запросов
fronts = [front_1, front_2]

# Словарь урлов и какие контроллеры по ним будут отрабатывать.
routes = {
    '/': Index(),
    '/index/': Index(),
    '/contact/': Contact(),
}
