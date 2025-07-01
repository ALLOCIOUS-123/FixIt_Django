# FixItHub - Community Problem Reporting System

A web application built with Django that allows users to report problems, submit solutions, and collaborate on fixing issues in their community.

## Features

- User Authentication with Email Verification
- Problem Reporting with Location Tracking
- Solution Submission and Voting
- Responsive Design with Bootstrap
- Email Verification System
- User Dashboard

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- SQLite (default) or PostgreSQL

## Installation and Setup

### Windows Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fixithub_django
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment file:
   ```bash
   copy .env.example .env
   ```

5. Edit .env file with your configurations:
   - Set DEBUG=True for development
   - Configure database settings
   - Set up email configurations
   - Add allowed hosts

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Linux Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fixithub_django
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   ```

5. Edit .env file with your configurations:
   - Set DEBUG=True for development
   - Configure database settings
   - Set up email configurations
   - Add allowed hosts

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
fixithub_django/
├── fixithub_django/           # Project configuration
├── fixithubapp/               # Main application
│   ├── migrations/            # Database migrations
│   ├── static/                # Static files
│   ├── templates/             # HTML templates
│   └── emails/                # Email templates
├── manage.py                  # Django management script
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables
├── .env.example               # Example environment file
└── README.md                  # This file
```

## Environment Variables

Copy `.env.example` to `.env` and update the following variables:

```env
# Basic Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@fixithub.com
FRONTEND_URL=http://127.0.0.1:8000

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## Running Tests

```bash
python manage.py test
```

## Deployment

1. Update `.env` with development settings:
   - Set DEBUG=True
   - Configure database settings
   - Set up email configurations
   - Add localhost to ALLOWED_HOSTS:
     ```env
     ALLOWED_HOSTS=localhost,127.0.0.1
     ```

2. Update frontend URL in `.env`:
   ```env
   FRONTEND_URL=http://127.0.0.1:8000
   ```

3. Configure SSL/HTTPS:
   - Obtain SSL certificate from Let's Encrypt
   - Configure your web server (Nginx/Apache) for HTTPS

4. Set up database:
   - Use PostgreSQL in production
   - Update database settings in `.env`:
     ```env
     DATABASE_URL=postgres://user:password@localhost:5432/fixithub_db
     ```

5. Configure email:
   - Use SendGrid or similar service
   - Update email settings in `.env`:
     ```env
     EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
     EMAIL_HOST=smtp.sendgrid.net
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER=your_sendgrid_username
     EMAIL_HOST_PASSWORD=your_sendgrid_password
     DEFAULT_FROM_EMAIL=noreply@fixithub.coo.ke
     ```

6. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

7. Apply migrations:
   ```bash
   python manage.py migrate
   ```

8. Start the production server (using Gunicorn as an example):
   ```bash
   gunicorn fixithub_django.wsgi:application
   ```

9. Configure Nginx (example configuration):
   ```nginx
   server {
       listen 80;
       server_name fixithub.coo.ke www.fixithub.coo.ke;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name fixithub.coo.ke www.fixithub.coo.ke;

       ssl_certificate /etc/letsencrypt/live/fixithub.coo.ke/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/fixithub.coo.ke/privkey.pem;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /path/to/your/staticfiles/;
       }

       location /media/ {
           alias /path/to/your/mediafiles/;
       }
   }
   ```

## SSL Certificate Setup

1. Install Certbot:
   ```bash
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d fixithub.coo.ke -d www.fixithub.coo.ke
   ```

3. Set up automatic renewal:
   ```bash
   sudo systemctl enable certbot-renew.timer
   sudo systemctl start certbot-renew.timer
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Features

- User authentication with email verification
- Problem submission with photo upload
- Solution sharing and voting
- Real-time notifications
- Search and filtering
- Responsive design

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required
DJANGO_SECRET=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgres://user:password@localhost:5432/fixithub

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## Deployment

The application is ready for deployment on platforms like Heroku or DigitalOcean. Make sure to:

1. Set `DEBUG=False` in your environment variables
2. Configure your production database
3. Set up proper SSL/TLS certificates
4. Configure email backend for production
5. Set up proper caching and session settings
