from django.db import models

FORBIDDEN_WORDS = [  # запрещённые к вводу в карточку товара слова
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

MAX_IMAGE_SIZE_BYTES = 5242880  # Максимальный размер загружаемого файла изображения в карточку товара в байтах
TYPE_OF_IMAGE = ['JPEG', 'PNG']  # Допустимый формат загружаемого файла изображения в карточку товара

FIELD_ATTRIBUTES = {  # Настройка атрибутов в соответствии типам полей
    models.CharField: {'class': 'form-control', 'placeholder': 'текст'},
    models.EmailField: {'class': 'form-control', 'type': 'email', 'placeholder': 'почта'},
    models.DateTimeField: {'class': 'form-control', 'type': 'datetime-local'},
    models.ForeignKey: {'class': 'form-select'},
    models.BooleanField: {'class': 'form-check-input'},
    models.ImageField: {'class': 'form-control-file', 'accept': 'image/*'},
}

REPLACEMENT_PLACEHOLDERS = {  # замена подсказок для пользователя в визуальных полях ввода: карточки
    # товара, карточки сообщения
    'email': 'почту',
    'price': 'цену в руб.',
    'username': 'имя',
    'phone': 'номер телефона'
    }

CATALOG_GROUP_LIST = ['Модератор продуктов']

FIXTURES_DICT = {  # словарь для создания фикстур пользователей и данных БД проекта
    'first_load_users_groups.json' : ['auth.Group', 'auth.User'],
    'second_load_apps_data.json' : ['catalog', 'blog']
    }