# Спортивные тренировки — FastAPI + PostgreSQL

Небольшой учебный REST API: участники, тренировки и записи на занятия.
Ровно **10 бизнес-операций**. Swagger и OpenAPI предоставляются FastAPI отдельно.

## Запуск в Docker

Из папки проекта при запущенном Docker Desktop:

```sh
docker compose up --build -d
docker compose ps
```

- Swagger: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- OpenAPI: http://localhost:8001/openapi.json
- Пример ответа: http://localhost:8001/workouts

Два сервиса: `backend` (Python 3.12 + FastAPI) и `postgres` (PostgreSQL 16).
Порт API 8001 открыт только на локальном компьютере (внутри контейнера — 8000).
БД доступна внутри сети Compose.
Учебные реквизиты БД: пользователь `workouts`, пароль `workouts_dev`, база `workouts`.

```sh
docker compose logs backend
docker compose exec postgres psql -U workouts -d workouts -c '\dt'
docker compose down
```

`down` сохраняет том БД. SQL из `sql/001_init.sql` выполняется только при первой
инициализации пустого тома. Изменения SQL не применяются автоматически к существующей БД.

## Как устроены данные

**API пока не подключается к PostgreSQL:** нет SQL-запросов, ORM и драйвера БД.
Готовые моки лежат в `app/mocks.py`: 2 участника, 2 тренировки и 1 запись.
GET возвращает эти данные. POST возвращает переданные поля с примерным ID,
PATCH возвращает пример изменённого объекта, DELETE — пустой ответ 204.
**Изменения не сохраняются:** следующий GET вернёт исходные моки.
ID в ответах POST фиксированные: 3 для участника/тренировки, 2 для записи.
PostgreSQL содержит три пустые таблицы, его данные сохраняются в томе независимо от API.
Остановка PostgreSQL не мешает работе API.

Хранилища, счётчиков ID и блокировок нет. Это заглушки для демонстрации REST API.

| Таблица | Поля |
|---|---|
| `participants` | `id INTEGER`, `name VARCHAR(100)`, `email VARCHAR(255)`, `created_at TIMESTAMPTZ` |
| `workouts` | `id INTEGER`, `title VARCHAR(100)`, `trainer_name VARCHAR(100)`, `starts_at TIMESTAMPTZ`, `duration_minutes INTEGER`, `capacity INTEGER` |
| `registrations` | `id INTEGER`, `participant_id INTEGER`, `workout_id INTEGER`, `created_at TIMESTAMPTZ` |

Все поля NOT NULL. PK генерируются как IDENTITY. Email уникален.
`registrations.participant_id` → `participants.id`,
`registrations.workout_id` → `workouts.id`: связь многие ко многим.
Пара `(participant_id, workout_id)` уникальна. Продолжительность и вместимость > 0.
Удаление родительской строки с существующими записями запрещено внешними ключами.

API возвращает те же поля, что таблицы: целые числа остаются числами,
даты передаются строками ISO 8601 с часовым поясом. В POST не передаются id/created_at.
Проверки свободных мест, повторной записи и существования связанных объектов
в POST пока не выполняются. Ограничения в SQL относятся к будущей работе с БД.

## Ручки

| Метод | Путь | Действие |
|---|---|---|
| GET | `/participants` | Список участников |
| POST | `/participants` | Создать участника |
| GET | `/participants/{id}` | Получить участника |
| GET | `/workouts` | Список тренировок |
| POST | `/workouts` | Создать тренировку |
| GET | `/workouts/{id}` | Получить тренировку |
| PATCH | `/workouts/{id}` | Обновить отдельные поля тренировки |
| GET | `/registrations` | Список записей |
| POST | `/registrations` | Записать участника |
| DELETE | `/registrations/{id}` | Отменить запись |

Фильтры: `/registrations?participant_id=1&workout_id=1`. Можно указать любой из
фильтров либо оба (условие AND). Отсутствие совпадений возвращает пустой список.

POST → 201, GET/PATCH → 200, DELETE → 204 без тела.
Ошибки: 404 — запрошенного объекта нет среди моков; 422 — неверный формат данных.
Неизвестные поля запрещены. PATCH не принимает null; пустой объект ничего не меняет.

## Примеры для Swagger

Создать участника (`POST /participants`):

```json
{"name": "Ольга", "email": "olga@example.com"}
```

Создать тренировку (`POST /workouts`):

```json
{
  "title": "Пилатес",
  "trainer_name": "Мария Иванова",
  "starts_at": "2027-01-22T18:00:00+05:00",
  "duration_minutes": 60,
  "capacity": 12
}
```

Пример записи участника (`POST /registrations`, ответ не сохраняется):

```json
{"participant_id": 2, "workout_id": 1}
```

Пример изменения вместимости (`PATCH /workouts/1`, ответ не сохраняется):

```json
{"capacity": 15}
```

## Локальный запуск

Python 3.12+; команды для PowerShell:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8001
```

Если используете `uv`: `uv venv --python 3.12`, затем `uv pip install -r requirements.txt`.

## Файлы

- `app/main.py` — 10 простых обработчиков.
- `app/schemas.py` — модели запросов и ответов Pydantic.
- `app/mocks.py` — готовые моки в обычных списках и словарях.
- `sql/001_init.sql` — схема PostgreSQL, ограничения и индекс.
- `Dockerfile`, `compose.yaml` — контейнеры.
