# TableFlow — Restaurant Table Reservation & Queue Management System

A full web system built with **Django + Channels** featuring:
- Responsive UI/UX (Bootstrap 5 + custom CSS)
- Sign up / sign in (secure password hashing + sessions)
- Customer portal (manage reservations)
- Reservation system w/ real-time availability checks (AJAX)
- Menu page with categories + item detail pages
- Live chat (WebSockets)
- Live announcements board (WebSockets)
- Admin dashboard (occupancy, peak hours, average wait)
- Django Admin for data management
- WSGI + ASGI included for deployment

## Quick start (dev)

1. Create venv and install deps
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create `.env`
   ```bash
   cp .env.example .env
   ```

3. Run migrations + create admin user
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. (Recommended) Run Redis (for WebSockets)
   - Install Redis locally, or run via Docker:
   ```bash
   docker run -p 6379:6379 redis:7
   ```

5. Start server
   ```bash
   python manage.py runserver
   ```

Visit:
- Home: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/
- Admin Dashboard: http://127.0.0.1:8000/dashboard/
- Live Board: http://127.0.0.1:8000/live/
- Live Chat: http://127.0.0.1:8000/chat/

## Deployment notes

- HTTP pages can run under **WSGI** (Gunicorn/uWSGI) using `restaurant_system/wsgi.py`
- WebSockets require **ASGI** (Daphne/Uvicorn) using `restaurant_system/asgi.py`
- In production, use Postgres and a Redis instance.

## Seed sample data (optional)

After migrations, run:
```bash
python manage.py seed_demo
```

