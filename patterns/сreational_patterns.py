from copy import deepcopy
from quopri import decodestring


# Абстрактный пользователь
class User:
    pass


# Пекарь
class Baker(User):
    pass


# Покупатель
class Client(User):
    pass


class UserFactory:  # Это не сама фабрика, это название класса
    types = {
        'client': Client,
        'baker': Baker
    }

    # Порождающий паттерн: Фабричный метод
    @classmethod
    def create(cls, type_):
        """
        Создание объекта пользователя конкретной сущности
        :param type_: название
        :return:
        """
        return cls.types[type_]()


# Порождающий паттерн Прототип
class PiePrototype:
    # Прототип пирожков

    def clone(self):
        return deepcopy(self)


class Pie(PiePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        # У категории есть входящие в неё пирожки, т.е. мы вносим объект этого пирожка в список пирожков категории
        self.category.pies.append(self)


# Пирожки открытые
class OpenPie(Pie):
    pass


# Пирожки закрытые
class ClosedPie(Pie):
    pass


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


# Движок - главный класс, где происходит создание всех объектов (основной интерфейс проекта)
class Engine:
    def __init__(self):
        self.bakers = []
        self.clients = []
        self.pies = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        """Создание пользователей"""
        return UserFactory.create(type_)

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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        """Вывод сообщения в терминал"""
        print('log--->', text)
