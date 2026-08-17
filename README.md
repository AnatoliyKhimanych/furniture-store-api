# Furniture Store REST API

REST API для мебельного магазина на **Django REST Framework**.

Сервис позволяет просматривать каталог мебели, получать информацию о конкретном товаре, создавать заказы и получать список заказов клиента по email.

## Стек

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL 16
- Docker
- Docker Compose

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd furnitureStore
```

### 2. Создать файл `.env`

В корне проекта создайте файл `.env`:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=1

DB_NAME=furniture
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

> `.env` содержит локальные настройки и секреты и не должен попадать в Git.

### 3. Собрать и запустить контейнеры

```bash
docker compose up -d --build
```

Будут запущены:

- Django API — `http://localhost:8000`
- PostgreSQL — порт `5432`

### 4. Выполнить миграции

После запуска контейнеров выполните:

```bash
docker compose exec web python manage.py migrate
```

После этого API готов к работе.

## API endpoints

### Получить весь список мебели

```http
GET /furniture/
```

Пример запроса:

```text
http://localhost:8000/furniture/
```

Пример ответа:

```json
[
  {
    "id": 1,
    "name": "Стол",
    "price": "100.00",
    "category": "table"
  },
  {
    "id": 2,
    "name": "Стул",
    "price": "50.00",
    "category": "chair"
  }
]
```

### Получить конкретный товар по ID

```http
GET /furniture/<id>/
```

Пример:

```text
http://localhost:8000/furniture/1/
```

Если товар с указанным ID не существует, API вернёт `404 Not Found`.

### Создать заказ

```http
POST /orders/
```

Тело запроса:

```json
{
  "email": "client@example.com",
  "goods": [1, 2]
}
```

Где:

- `email` — email клиента;
- `goods` — список ID товаров.

Общая сумма заказа рассчитывается автоматически на сервере на основе стоимости выбранных товаров.

При создании заказа API проверяет:

- наличие `email`;
- корректность email;
- наличие списка `goods`;
- что список товаров не пуст;
- что ID товаров являются положительными целыми числами;
- отсутствие повторяющихся ID;
- существование переданных товаров в базе данных.

### Получить заказы клиента

```http
GET /orders/?email=<email>
```

Пример:

```text
http://localhost:8000/orders/?email=client@example.com
```

Пример ответа:

```json
{
  "id": 1,
  "email": "client@example.com",
  "amount": "150.00",
  "date": "2026-08-17T12:00:00Z",
  "goods_list": [1, 2]
}
```

Параметр `email` обязателен.

## Дополнительно реализовано

Поддерживается фильтрация мебели по категории:

```http
GET /furniture/?category=table
```

Доступные категории:

- `table` — стол;
- `chair` — стул;
- `sofa` — диван.

Пример:

```text
http://localhost:8000/furniture/?category=sofa
```

## Остановка проекта

```bash
docker compose down
```

Чтобы также удалить Docker volume с данными PostgreSQL:

```bash
docker compose down -v
```
