# E-commerce Store

## Overview
This project is a comprehensive e-commerce platform built with Django. It offers a solid foundation for online stores, featuring user authentication, product management, shopping cart functionality, order processing, coupon discounts, and RESTful APIs. The application is modular, scalable, and designed for easy customization.

## Features
- User registration, login, and email activation
- Product catalog with categories, search, and detailed product pages
- Shopping cart with add, remove, and update capabilities
- Order creation and payment processing (including Vodafone Cash integration)
- Coupon system for discounts
- Admin PDF invoice generation
- RESTful API endpoints for products, categories, and user management
- Asynchronous email and invoice sending with Celery
- JWT authentication for secure API access
- Responsive frontend using Django templates and crispy forms

## Tech Stack
- **Backend:** Django 5.2, Django REST Framework
- **Database:** PostgreSQL
- **Task Queue:** Celery, Redis
- **Frontend:** Django Templates, crispy-bootstrap4
- **PDF Generation:** WeasyPrint
- **Other:** psycopg2, pycountry, Pillow, and more (see `requirements.txt`)

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for Celery)

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd E-commerce
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the database:**
   - Update `src/settings.py` with your PostgreSQL credentials if needed.
   - Create the database (default name: `store`).
5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run Redis and Celery (for async tasks):**
   - Start the Redis server.
   - In a new terminal, run:
     ```bash
     celery -A src worker --loglevel=info
     ```
8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the site at `http://localhost:8000/`
- Admin panel: `http://localhost:8000/admin/`
- API endpoints: `http://localhost:8000/v1/api/`
- Obtain JWT token: `http://localhost:8000/api/token/`

## Project Structure
```
E-commerce/
├── accounts/      # User authentication and profiles
├── apis/          # REST API endpoints
├── cart/          # Shopping cart logic
├── coupons/       # Coupon/discount system
├── order/         # Order and payment processing
├── store/         # Product catalog and categories
├── src/           # Project settings, static, templates
├── templates/     # HTML templates
├── static/        # Static files (CSS, JS, images)
├── media/         # Uploaded media files
└── requirements.txt
```

## Notes
- Make sure to configure email settings in `src/settings.py` for account activation and order notifications.
- For production, set `DEBUG = False` and update `ALLOWED_HOSTS`.
- Static and media files are served locally in development; configure proper storage for production.

## License
This project is for educational and demonstration purposes. Please review and update the license as needed for your use case.
