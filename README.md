# Hotel Reservation System - Morocco

A modern web application for managing hotel reservations in Morocco, built with Django and MySQL.

## Features

- User authentication (login/register)
- Room browsing and availability checking
- Reservation management
- Admin dashboard for hotel management
- Responsive design for all devices
- Support for Moroccan cities and regions
- Multilingual support (English, French, Arabic)
- Moroccan currency (MAD) support

## Setup Instructions

1. **Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **MySQL Database Setup:**
   - Create a new database in PHPMyAdmin or MySQL named `hotel_reservation`
   - Set up your MySQL user credentials (update `hotel_reservation/settings.py` if needed)

4. **Configure Django settings:**
   - In `hotel_reservation/settings.py`, set your database credentials under `DATABASES`.
   - Set `SECRET_KEY` and other environment-specific settings as needed.

5. **Apply migrations to initialize the database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser for the admin dashboard:**
```bash
python manage.py createsuperuser
```

7. **Run the development server:**
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Project Structure

```
hotel_reservation/
├── reservations/
├── users/
├── hotel_reservation/
├── manage.py
├── requirements.txt
├── venv/
├── static/
├── media/
└── README.md
```

## Supported Cities

The system includes support for major Moroccan cities including:
- Casablanca
- Marrakech
- Rabat
- Fes
- Tangier
- Agadir
- Essaouira
- Chefchaouen
- And more... 