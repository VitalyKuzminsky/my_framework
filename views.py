# Контроллеры

from datetime import date
from my_framework.template_engine import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


# Контакты
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


# О проекте
class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html', date=request.get('date', None))


# Ошибка 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


# Пирожковая
class Bakery:
    def __call__(self, request):
        return '200 OK', render('bakery.html', date=date.today())


# Список пирожков
class PiesList:
    def __call__(self, request):
        logger.log('Список пирожков')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('pie_list.html',
                                    objects_list=category.pies,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No pies have been added yet'


# Создать пирожок
class CreatePie:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # Метод POST
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                pie = site.create_pie('closed', name, category)
                site.pies.append(pie)

            return '200 OK', render('pie_list.html',
                                    objects_list=category.pies,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_pie.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Создание категории
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # Метод POST

            data = request['data']

            name = data['name']  # Имя
            name = site.decode_value(name)  # Декодируем

            category_id = data.get('category_id')

            category = None  # Если подкатегории нет, то None

            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)  # Создание новой категории

            site.categories.append(new_category)  # Вносим в список категорий движка

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)  # Здесь видны все категории


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# Копировать пирожок
class CopyPie:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_pie = site.get_pie(name)
            if old_pie:
                new_name = f'copy_{name}'
                new_pie = old_pie.clone()
                new_pie.name = new_name
                site.pies.append(new_pie)

            return '200 OK', render('pie_list.html',
                                    objects_list=site.pies,
                                    name=new_pie.category.name)
        except KeyError:
            return '200 OK', 'No pies have been added yet'
