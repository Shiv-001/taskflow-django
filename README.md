# Taskflow — Personal Task Tracker

A clean, full-featured task tracker built with Django.

## Features
- User registration & authentication
- Create, edit, delete tasks
- Priority levels: Low, Medium, High, Urgent
- Status tracking: To Do, In Progress, Done
- Categories with custom colors
- Due dates with overdue detection
- Filter by status, priority, category
- Search tasks by title/description
- Quick toggle tasks complete/incomplete
- Stats dashboard (total, todo, in progress, done, overdue)

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. (Optional) Create a superuser for the admin panel
```bash
python manage.py createsuperuser
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open your browser
Visit: http://127.0.0.1:8000

Register a new account and start adding tasks!

## Admin Panel
Visit http://127.0.0.1:8000/admin/ and log in with your superuser credentials to manage all data.

## Project Structure
```
tasktracker/
├── manage.py
├── requirements.txt
├── tasktracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/
    ├── models.py       # Task, Category models
    ├── views.py        # All views
    ├── forms.py        # Forms
    ├── urls.py         # URL routing
    ├── admin.py        # Admin config
    ├── migrations/
    └── templates/tasks/
        ├── base.html
        ├── dashboard.html
        ├── task_form.html
        ├── task_confirm_delete.html
        ├── categories.html
        ├── login.html
        └── register.html
```
