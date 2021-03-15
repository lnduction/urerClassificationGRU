import vk_api
from googletrans import Translator
import re
import emoji


def reading(id):

    max_post = 20       # Максимальное считывание постов
    translator = Translator()

    # Считывание логина и пороля из файла
    file = open('project/files/authorization')
    login = file.readline()
    password = file.readline()
    file.close()

    # Получение сессии
    vk_session = vk_api.VkApi(login, password)

    # отлавливание ошибок при авторизации
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    # Парсинг страницы vk
    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all('wall.get', 100, {'owner_id': id})

    # Запись постов в файл
    if wall['count']:
        file = open('project/files/posts.txt', 'w')
        for i in range(0, wall['count']):
            post = wall['items'][i].get('text')
            if not post:
                continue
            post = strip_emoji(post)
            post = strip_links(post)
            result = translator.translate(post, 'en', 'ru')
            post = result.text
            file.write(post)
            if i == max_post:
                break
        file.close()


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text
