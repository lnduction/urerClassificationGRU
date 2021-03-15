from keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GRU
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import utils
import pandas as pd
import pickle

# Необходимый кусок кода для избежани ошибок
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def training():
    # Обьявляем константы
    num_words = 10000               # Максимальное количество слов
    max_post_len = 100              # Максимальная длина постов
    nb_classes = 4                  # Количество классов постов

    # Читаем данные из файла
    train = pd.read_csv('project/files/train.csv', header=None, names=['class', 'title', 'text'])

    # Выделяем данные для обучения
    posts = train['text']

    # Выделяем правильные ответы
    y_train = utils.to_categorical(train['class'] - 1, nb_classes)

    # Токенизация текста # Создаем токенизатор Keras
    tokenizer = Tokenizer(num_words=num_words)

    # Обучаем токенизатор на посты
    tokenizer.fit_on_texts(posts)

    # Серелизация токенайзера
    file = open("project/files/tokenizer.txt", "wb")
    pickle.dump(tokenizer, file)
    file.close()

    # Преобразуем новости в числовое представление
    sequences = tokenizer.texts_to_sequences(posts)

    # Ограничиваем длину постов
    x_train = pad_sequences(sequences, maxlen=max_post_len)

    # Сеть GRU
    model_gru = Sequential()
    model_gru.add(Embedding(num_words, 32, input_length=max_post_len))
    model_gru.add(GRU(16))
    model_gru.add(Dense(4, activation='softmax'))
    model_gru.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Создаем callback для сохранения нейронной сети на каждой эпохе,
    # если качество работы на проверочном наборе данных улучшилось. Сеть сохраняется в файл `best_model_gru.h5`
    model_gru_save_path = 'project/files/best_model_gru.h5'
    checkpoint_callback_gru = ModelCheckpoint(model_gru_save_path, monitor='val_accuracy', save_best_only=True,
                                              verbose=1)
    history_gru = model_gru.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1,
                                callbacks=[checkpoint_callback_gru])

    # Загружаем набор данных для тестирования
    test = pd.read_csv('project/files/test.csv', header=None, names=['class', 'title', 'text'])

    # Преобразуем новости в числовое представление
    test_sequences = tokenizer.texts_to_sequences(test['text'])
    x_test = pad_sequences(test_sequences, maxlen=max_post_len)

    # Правильные ответы
    y_test = utils.to_categorical(test['class'] - 1, nb_classes)

    # Оцениваем качество работы сети на тестовом наборе данных
    model_gru.load_weights(model_gru_save_path)
    model_gru.evaluate(x_test, y_test, verbose=1)
