# Контроллеры

from datetime import date
from my_framework.template_engine import render
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
# from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer


site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()  # Новый поток для работы с БД
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)  # В текущем потоке связка с реестром

routes = {}  # Пустой словарь, который будет заполнять декоратор при открытии проекта


# Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        # return '200 OK', render('index.html', date=request.get('date', None))
        return '200 OK', render('index.html', objects_list=site.categories)


# Контакты
@AppRoute(routes=routes, url='/contact/')
class Contact:
    def __call__(self, request):
        # return '200 OK', render('contact.html', date=request.get('date', None))
        return '200 OK', render('contact.html')


# О проекте
@AppRoute(routes=routes, url='/about_us/')
class AboutUs:
    @Debug(name='AboutUs')
    def __call__(self, request):
        # return '200 OK', render('about_us.html', date=request.get('date', None))
        return '200 OK', render('about_us.html')


# Ошибка 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


# Пирожковая
@AppRoute(routes=routes, url='/bakery/')
class Bakery:
    @Debug(name='Bakery')
    def __call__(self, request):
        return '200 OK', render('bakery.html', objects_list=site.categories, date=date.today())


# Список пирожков
@AppRoute(routes=routes, url='/pies_list/')
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
@AppRoute(routes=routes, url='/create_pie/')
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

                pie = site.create_pie('closed', name, category)  # Создание нового пирожка

                # Обратившись к пирожку и его наблюдателю добавить туда наблюдателей
                pie.observers.append(email_notifier)
                pie.observers.append(sms_notifier)

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
@AppRoute(routes=routes, url='/create_category/')
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
@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# Копировать пирожок
@AppRoute(routes=routes, url='/copy_pie/')
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


@AppRoute(routes=routes, url='/client_list/')
class ClientListView(ListView):
    template_name = 'client_list.html'

    def get_queryset(self):
        """Через наш реестр получает нужный mapper по названию таблицы"""
        mapper = MapperRegistry.get_current_mapper('client')
        return mapper.all()  # возвращает всё - список объектов модели


@AppRoute(routes=routes, url='/create_client/')
class ClientCreateView(CreateView):
    template_name = 'create_client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('client', name)
        site.clients.append(new_obj)  # добавление объекта в список
        new_obj.mark_new()  # Помечаем, как новый
        UnitOfWork.get_current().commit()  # Коммитим - данные пошли в БД


@AppRoute(routes=routes, url='/add_client/')
class AddClientByPieCreateView(CreateView):
    template_name = 'add_client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['pies'] = site.pies
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        pie_name = data['pie_name']
        pie_name = site.decode_value(pie_name)
        pie = site.get_pie(pie_name)
        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_client(client_name)
        pie.add_client(client)


@AppRoute(routes=routes, url='/api/')
class PieApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.pies).save()
