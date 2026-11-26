# Helpdesk — варіант 13

Навчальний проєкт служби підтримки: Django + DRF та незалежний FastAPI SLA/Classification Service.

## Запуск
1. Встановіть Docker Desktop.
2. У корені проєкту виконайте `docker compose up --build`.
3. Django: http://localhost:8001 ; API: http://localhost:8001/api/tickets/ ; FastAPI docs: http://localhost:8000/docs ; health: http://localhost:8000/health.

## Django
Після запуску контейнера виконайте `docker compose exec django python manage.py createsuperuser`. API використовує JWT: POST `/api/token/` (username/password), refresh `/api/token/refresh/`.

Основні API: `/api/tickets/`, `/api/comments/`, `/api/articles/`; дії `tickets/{id}/assign`, `tickets/{id}/transition`, `tickets/overdue/`. Підтримуються фільтри status, priority, agent та пошук title/description.

## FastAPI
`/sla/track`, `/sla/breaches`, `/classify`, `/sla/escalate`, WebSocket `/ws/tickets/{id}`, `/health`. Класифікатор використовує демонстраційні ключові слова, не ML.

## Модель
Customer, Agent, Category, Priority, Tag, Ticket, Comment, Attachment, SLAPolicy, KnowledgeArticle, CSAT.

## Примітки
Це базова навчальна реалізація, не готова до production. Перед здачею варто доповнити Django/FastAPI тестами, Alembic-міграціями, повноцінною рольовою перевіркою, SLA webhook-інтеграцією, реальним Redis-кешуванням, Nginx конфігурацією/healthchecks, CSRF/лімітами upload, CI, ER-діаграмами та seeded data. Використання генерації коду зазначайте відповідно до методички.
