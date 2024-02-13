# Yatube
## Описание


Полноценная социальная сеть, cпроектированная с помощью Djnago


## Технологии
- Python 3.11
- Django 2.2.19

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VladimirKarpenkoMain/Yatube
```

```
cd Yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Автор
Владимир Карпенко
