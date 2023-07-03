# Запуск сервера

from wsgiref.simple_server import make_server
from my_framework.main import MyFramework
from urls import fronts
from views import routes

# from urls import routes  # импорт с 5 урока не нужен

application = MyFramework(routes, fronts)

with make_server('', 8000, application) as httpd:
    print('Simple server запущен удачно! Локальный хост, порт 8000')
    httpd.serve_forever()
