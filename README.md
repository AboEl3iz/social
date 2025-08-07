# SocialHub

A mini Facebook-like social media platform built with Django 5.2+.

## Features
- User registration, login, logout, and password reset (with email)
- User profiles with bio and avatar
- Create, view, like/unlike, and comment on posts
- Privacy and email notification settings
- Responsive Bootstrap UI
- Image uploads (Pillow)
- AJAX like/unlike
- Custom 404 and error pages

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Create a `.env` file in the project root:**
   ```
   SECRET_KEY=your-django-secret-key
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-gmail-address@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```
5. **Apply migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create a superuser (optional, for admin access)**
   ```
   python manage.py createsuperuser
   ```
7. **Run the development server**
   ```
   python manage.py runserver
   ```
8. **Access the app at** `http://127.0.0.1:8000/`

## Notes
- For email features, use a Gmail account and an app password.
- Media uploads are stored in the `media/` directory.
- Static files are served from the `static/` directory.

---

Enjoy SocialHub!