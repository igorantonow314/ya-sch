# Тестовое задание [Школы бэкенд-разработки Яндекса](https://academy.yandex.ru/schools/backend)

Это выполненное мной тестовое задание [Школы бэкенд-разработки Яндекса](https://academy.yandex.ru/schools/backend).

[Изначально](https://github.com/igorantonow314/ya-sch/tree/409abfb27a81c1dacd687f2869251bd64e0df7d9) были даны: описание задания (файл [Task.md](Task.md)), файл [openapi.yaml](openapi.yaml) (tip: [swagger.io](https://editor.swagger.io/)), и примеры тестов ([unit_test.py](unit_test.py)).

Для деталей задания **рекомендую ознакомиться с файлом [Task.md](Task.md).**

Всё, за исключением этого файла, я сделал за два дня. Поэтому задание выполнено не идеально, и кое-что не доделано (например, я не описал, как сделать свой systemd unit, успел лишь настроить конкретно для своего компа и для сервера). 



### Развёртывание и разработка

Все инструкции приводятся для linux. Использовался `python3.8+`, но, возможно, подойдёт и более ранняя версия.

##### Скачивание
```bash
git clone https://github.com/igorantonow314/ya-sch#
cd ya-sch
```

##### Установка (минимальная):
```bash
python -m pip install -r requirements.txt
```
##### Запуск:
```bash
python .
```

##### Установка (для разработки):
```bash
make install
```

##### Тестирование
```bash
make test
```

Корректировка и проверка форматирования кода:
```bash
make lint
```
(используются `black` и `flake8`)


### Структура проекта

- `api/` - модуль, отвечающий за реализацию api
  - `app.py` - основные методы api, собственно сервер (`aiohttp`)
  - `shema.py` - схема(-ы) для валидации приходящих запросов
- `db/` - модуль, отвечающий за базу данных (исп. `sqlalchemy` )
  - `db.py`

- `shop.db` - база данных в формате `sqlite`

- `unit_test.py` - тестирование API запущенного проекта
- `unit_test.sh` - полезный скрипт, который запускает проект, тестирует api, и прекращает выполнение проекта
- `tests/` - другие тесты, тестирующие непосредственно функции модулей, с использованием `pytest`

- Временные файлы:
	- `htmlcov/index.html` - отчёт покрытия кода тестами из `tests/` (на момент релиза только `db.py` на 93%)
	- `expected.json`, `response.json` - см. `unit_test.py`
	- `test-db.db` - база данных, созданная во время тестирования `tests/db/db.py`

- `Task.md` - описание задания
- `openapi.yaml` - описание спецификации API
- `.gitignore`, `.flake8`, `pytest.ini` - конфигурационные файлы соответствующих утилит