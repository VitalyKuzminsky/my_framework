from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Производит рендеринг шаблона страницы.

    :param template_name: Имя шаблона.
    :param folder: Папка в которой находиться шаблон.
    :param kwargs: Параметры, передаваемые в шаблон.
    :return: Рендеринг.
    """

    # Создаем объект окружения
    env = Environment()

    # Назначаем папку, где находятся наши шаблоны
    env.loader = FileSystemLoader(folder)

    # Находим шаблон в окружении по имени
    template = env.get_template(template_name)

    # Рендерим с параметрами, передаваемыми в шаблон
    return template.render(**kwargs)
