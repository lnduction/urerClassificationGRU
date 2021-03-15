from django.shortcuts import render
from vk_api import VkToolsException
from project.read_posts import reading
from project.work_neural_network import nn


# Загрузка главной страницы
def ranger_page(request):
    return render(request, 'main.html')


# Функция, которую вызывает форма
def classification(request):

    # Получение id пользователя из POST запроса
    user_id = request.POST.get('user_id')
    # Случай нажатия кнопки без ввода id
    if not user_id:
        return render(request, 'main.html')
    # Отлавнивание ошибок при парсинге
    try:
        reading(user_id)
    except VkToolsException:
        result = {'error': 'Неверный id, либо пользователь закрыл доступ к своей странице'}
        return render(request, 'main.html', result)

    # Прогоняем посты через нейросеть
    result = nn("project/files/posts.txt")

    # Находим группу интереса по результату
    if result[0] == 1:
        post = "Интересуется миром"
    elif result[1] == 1:
        post = "Интересуется спортом"
    elif result[2] == 1:
        post = "Интересуется бизнесом"
    elif result[3] == 1:
        post = "Интересуется наукой"
    else:
        # Отлавливаем возможные ошибки
        error = "Ошибка"
        result = {'error': error}
        return render(request, 'main.html', result)

    # Формируем результат
    result = {'posts': post,
              'phrase': "Этот пользователь: "}

    return render(request, 'main.html', result)
