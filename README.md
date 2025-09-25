📊 Monitoring System
Простая система мониторинга серверов с веб-интерфейсом, сбором метрик (CPU, RAM, Disk, Uptime) и обработкой инцидентов.
Проект написан на Django + Celery + MySQL, контейнеризирован с помощью Docker Compose.

🚀 Возможности
Сбор метрик с машин (CPU, память, диск, uptime).
Хранение истории метрик в базе данных.
Автоматическая проверка пороговых значений и создание инцидентов.
Веб-интерфейс для просмотра метрик и инцидентов.
Админ-панель Django для управления машинами и инцидентами.
Поддержка фоновых задач через Celery.

⚙️ Технологии
Python 3.12
Django 5
Celery + Redis
MySQL 8
Docker / Docker Compose

1. Клонирование проекта
    ```bash
    git clone https://github.com/yourname/monitoring.git
    cd monitoring
    ```
2. Собрать и запустить контейнеры
   ```
   docker compose up --build -d
   ```
4. Выполнить миграции и создать суперпользователя
   ```
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
  Доступ:
    Веб-интерфейс: http://localhost:8000/metric/view/incident
    Админка: http://localhost:8000/admin
5. Запуск задач Celery
   Celery запускается автоматически через docker compose:
    celery_worker - выполняет задачи(fetch_metrics, проверки инцидентов)
    celery_beat - планироващикб переодически запускающий проверки
    Проверить логи:
  ```
    docker compose logs -f celery_worker
    docker compose logs -f celery_beat
  ```
6.Тесты
  Запуск unit-тестов:
  ```
  docker compose exec web python manage.py test
  ```
