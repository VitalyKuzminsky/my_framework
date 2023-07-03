from datetime import date
from views import Index, Contact, AboutUs, Bakery, PiesList, \
    CreatePie, CreateCategory, CategoryList, CopyPie


# Реализация Front controller
def front_1(request):
    request['Пасхалка_1'] = 'Hello World!'


def front_2(request):
    request['Пасхалка_2'] = 'Все запросы работают с Front controller'


# Список фронтов для всех запросов
fronts = [front_1, front_2]

# Словарь урлов и какие контроллеры по ним будут отрабатывать.
# c 5 урока больше не нужен, теперь routes во views, наполняется декоратором
# routes = {
#     '/': Index(),
#     '/index/': Index(),
#     '/contact/': Contact(),
#     '/about_us/': AboutUs(),
#     '/bakery/': Bakery(),
#     '/pies_list/': PiesList(),
#     '/create_pie/': CreatePie(),
#     '/create_category/': CreateCategory(),
#     '/category_list/': CategoryList(),
#     '/copy_pie/': CopyPie(),
# }
