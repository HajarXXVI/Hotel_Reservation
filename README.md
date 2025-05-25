# Hotel Reservation System - Morocco

A modern web application for managing hotel reservations in Morocco, built with Flask and MySQL.

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

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. MySQL Database Setup:
   - Create a new database in PHPMyAdmin named `morocco_hotel_db`
   - Set up your MySQL user credentials

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@localhost/morocco_hotel_db
```

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
hotel_reservation/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── migrations/
├── venv/
├── .env
├── requirements.txt
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