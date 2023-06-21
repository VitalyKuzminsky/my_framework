# Контроллеры - пока только главная страница и контакты

from my_framework.template_engine import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html', date=request.get('date', None))
