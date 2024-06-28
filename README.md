# Modsen Practice

## Проекты

Этот репозиторий содержит проекты, выполненные в качестве практики. Ниже приведены краткие описания каждого проекта.

### 1. Image Recognition

Этот проект включает скрипт для поиска дубликатов изображений в указанных папках. Он использует модель VGG16 для извлечения признаков изображений и сравнения их по хэшам и признакам.

#### Основные функции:
- **Загрузка изображений**: Загрузка изображений из указанных папок.
- **Извлечение признаков**: Преобразование изображений в векторы признаков с помощью модели VGG16.
- **Поиск дубликатов**: Поиск дубликатов изображений на основе хэшей и признаков.
- **Отображение дубликатов**: Визуализация найденных дубликатов изображений.

#### Запуск:
```bash
python main.py <путь_к_папке1> [<путь_к_папке2>]
```

### 2. HTTPWeatherAPI

Этот проект представляет собой простой веб-сервис, который проверяет различные статусы ответов от API OpenWeatherMap. Веб-сервис написан на Flask и предоставляет информацию о статусах запросов.

#### Основные функции:
- **Проверка статусов**: Отправка запросов к API OpenWeatherMap с различными параметрами и возвращение статусов ответов.
- **Обработка ошибок**: Обработка различных ошибок, таких как неверный API ключ, несуществующие данные и другие.

#### Запуск:
```bash
python app.py
```

После запуска сервис будет доступен по адресу `http://127.0.0.1:5000/status_codes`.

## Установка зависимостей

Для установки всех необходимых зависимостей выполните:
```bash
pip install -r requirements.txt
```

## Контакты

Для вопросов и предложений, пожалуйста, обращайтесь в Telegram: @w1ckedside