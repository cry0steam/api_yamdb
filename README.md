# APIYAMDB
## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

В работе реализована авторизация и аутентификация. Для аутентификации используются JWT-токены. У неаутентифицированных пользователей доступ к проекту имеется только на чтение. Аутентифицированным пользователям разрешено изменение и удаление своего контента.

**В процессе разработки были использованы технологии:**
- Django REST framework (DRF) 3.12
- Django 3.2
- Python 3.9


## Как запустить проект:

```
python -m venv venv
```
Если у вас Windows OS:
```
source venv/Scripts/activate
```
Если у вас MacOS/Linux:
```
source venv/bin/activate
```

```
python -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
python manage.py migrate
```

### Запустить проект:

```
python manage.py runserver
```

### Документация API
```
http://127.0.0.1:8000/redoc/
```

### Примеры работы с API для всех пользователей

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится. 

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
GET /api/v1/users/ - Получение списка всех пользователей
```

### Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

### Примеры работы с API для авторизованных пользователей

Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

### Авторы проекта

Студенты Яндекс Практикум, курс Python-Разработчик, когорта №92

```
Герман Коренблюм, Валерий Смирнов, Бессонов Денис
```
