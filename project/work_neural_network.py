from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GRU
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import utils
import pickle

# Важный кусок для избежании ошибок
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def nn(path):
    # Обьявление констант
    num_words = 10000           # Максимальное количество слов
    max_post_len = 100          # Максимальная длина поста
    nb_classes = 4              # Количество классов поста
    result = [0, 0, 0, 0]       # Результат

    # Считывание токинайзера из файла
    file = open("project/files/tokenizer.txt", "rb")
    tokenizer = pickle.load(file)
    file.close()

    # Сеть GRU
    model_gru = Sequential()
    model_gru.add(Embedding(num_words, 32, input_length=max_post_len))
    model_gru.add(GRU(16))
    model_gru.add(Dense(4, activation='softmax'))
    model_gru.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model_gru_save_path = 'project/files/best_model_gru.h5'

    # Открытие файла с постами
    file = open(path, 'r')
    # Считывание поста
    text = file.read()

    # Векторизация поста
    test_sequences = tokenizer.texts_to_sequences([text])
    post = pad_sequences(test_sequences, maxlen=max_post_len)

    # Загрузка весов нейросети
    model_gru.load_weights(model_gru_save_path)

    # Прогон поста через нейросеть
    for i in range(0, 4):
        # Представление категории в виде вектора
        category = utils.to_categorical([str(i)], nb_classes)
        # Получение убыли и точности
        acc = model_gru.evaluate(post, category, verbose=1)
        # Суммирование всех точностей
        result[i] += int(acc[1])

    return result
