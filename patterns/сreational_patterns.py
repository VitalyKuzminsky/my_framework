from copy import deepcopy
from quopri import decodestring
from datetime import datetime
from patterns.behavioral_patterns import Subject, FileWriter


# from behavioral_patterns import FileWriter, Subject


# Абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# Пекарь
class Baker(User):
    pass


# Покупатель
class Client(User):
    def __init__(self, name):
        self.pies = []
        super().__init__(name)


class UserFactory:  # Это не сама фабрика, это название класса
    types = {
        'client': Client,
        'baker': Baker
    }

    # Порождающий паттерн: Фабричный метод
    @classmethod
    def create(cls, type_, name):
        """
        Создание объекта пользователя конкретной сущности
        :param type_: название
        :param name: имя
        :return:
        """
        return cls.types[type_](name)


# Порождающий паттерн Прототип
class PiePrototype:
    # Прототип пирожков

    def clone(self):
        return deepcopy(self)


class Pie(PiePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        # У категории есть входящие в неё пирожки, т.е. мы вносим объект этого пирожка в список пирожков категории
        self.category.pies.append(self)
        self.clients = []
        super().__init__()

    def __getitem__(self, item):
        return self.clients[item]

    def add_client(self, client: Client):
        """Добавление нового клиента при создании объекта пирожка"""
        self.clients.append(client)  # вносим в список
        client.pies.append(self)
        # Если он добавляется, то уведомить всех подписчиков
        self.notify()


# Пирожки открытые
class OpenPie(Pie):
    pass


# Пирожки закрытые
class ClosedPie(Pie):
    pass


# Категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name  # Имя
        self.category = category  # Текущая категория является чьей-то подкатегорией.
        self.pies = []  # Входящие в категорию пирожки

    def pie_count(self):
        """"Пирожки входящие в список пирожков категории"""
        result = len(self.pies)
        if self.category:
            result += self.category.pie_count()
        return result


class PieFactory:
    types = {
        'open': OpenPie,
        'closed': ClosedPie
    }

    # Порождающий паттерн: Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        """
        Создание объекта пирожок конкретной сущности
        """
        return cls.types[type_](name, category)


# Движок - главный класс, где происходит создание всех объектов (основной интерфейс проекта)
class Engine:
    def __init__(self):
        self.bakers = []
        self.clients = []
        self.pies = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        """Создание пользователей"""
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        """Создание категорий"""
        return Category(name, category)

    def find_category_by_id(self, id):
        """Получение категории по id"""
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_pie(type_, name, category):
        """Создание пирожка"""
        return PieFactory.create(type_, name, category)

    def get_pie(self, name):
        """Получение пирожка по имени"""
        for item in self.pies:
            if item.name == name:
                return item
        return None

    def get_client(self, name) -> Client:
        """Получение клиента"""
        for item in self.clients:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        """Декодирование"""
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# Порождающий паттерн: Синглтон
class SingletonByName(type):
    # Нужен для создания логера, чтобы объект логера был всегда один и тот же.

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        """Вывод сообщения в файл"""
        text = f'log--> {datetime.now()}: {text}'
        self.writer.write(text)
