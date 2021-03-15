from django.urls import path

from project import view
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Передает запрос на функцию ranger_page в файле view
    path('', view.ranger_page, name='render_page'),
    # Передает запрос на функцию classification в файле view
    path('classification', csrf_exempt(view.classification), name='classification'),
]
