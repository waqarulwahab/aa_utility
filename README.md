# Modern Authentication System

A reusable, modern authentication system built with Django, featuring user registration with email verification (OTP), secure login, and password reset functionality.

## Features

- **User Registration**: Create an account with email and username
- **Email Verification**: Verify email address with a 6-digit OTP
- **Secure Login**: Authenticate users with email and password
- **Password Reset**: Recover account access via email
- **User Profile**: Update user information and profile picture
- **Responsive Design**: Modern UI that works on all devices
- **Reusable Architecture**: Easy to integrate into any Django project

## Color Scheme

- **Primary**: #2C3E50 (Dark Blue)
- **Secondary**: #E74C3C (Red)
- **Accent**: #F1C40F (Yellow)
- **Light**: #ECF0F1 (Light Gray)
- **Dark**: #34495E (Darker Blue)

## Fonts

- **Headings**: Playfair Display
- **Body**: Poppins

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.1+

### Installation

1. Clone the repository or download the source code
2. Create a virtual environment:

```bash
python -m venv auth_env
```

3. Activate the virtual environment:

**Windows**
```bash
auth_env\Scripts\activate
```

**macOS/Linux**
```bash
source auth_env/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Access the application at `http://127.0.0.1:8000/`

### Email Configuration

For development, the system uses Django's console email backend which prints emails to the console. For production, you'll need to configure SMTP settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## Integration

To integrate this authentication system into another Django project:

1. Copy the `user_auth` app to your project
2. Add `user_auth` to your `INSTALLED_APPS` in `settings.py`
3. Configure the authentication settings in `settings.py`:

```python
AUTH_USER_MODEL = 'user_auth.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
```

4. Include the URLs in your main `urls.py`:

```python
path('', include('user_auth.urls')),
```

5. Apply migrations for the app

## Customization

The authentication system is designed to be easily customizable:

- **Templates**: Modify the HTML templates in the `templates/user_auth` directory
- **Styles**: Customize CSS in the `static/css/style.css` file
- **User Model**: Extend the `CustomUser` model in `models.py` to add more fields
- **Email Content**: Update email templates in the `templates/user_auth/email` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django community for the amazing framework
- Bootstrap for responsive design components
- Google Fonts for Playfair Display and Poppins fonts
