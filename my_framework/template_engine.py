from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    """
    Производит рендеринг шаблона страницы.

    :param template_name: Имя шаблона.
    :param folder: Папка в которой находиться шаблон.
    :param kwargs: Параметры, передаваемые в шаблон.
    :return: Рендеринг.
    """

    # Путь до файла
    file_path = join(folder, template_name)

    # Открываем шаблон
    with open(file_path, encoding='utf-8') as f:

        # Читаем файла
        template = Template(f.read())

    # Рендеринг шаблона.
    return template.render(**kwargs)
