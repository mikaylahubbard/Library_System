## My Library Django App
A simple Django web app to manage books and users. Users can register, log in, browse available books, borrow and return them, and view their checked-out books. Data is stored in JSON files

### To Run
- clone the repo
- In Terminal: `pip install django`
- In Terminal: `python manage.py runserver`
- Browse to http://127.0.0.1:8000/

### Features
- User registration (students & teachers)
- Login and logout
- Browse books with availability status
- Borrow and return books
- View checked-out books

### Important Files
```
Library_App/
├── static/             # Images, CSS, JS
├── templates/          # HTML templates
├── models.py           # Python classes for User, Book, Library
├── views.py            # Django views
├── urls.py             # URL routing
├── books.json          # Book data
├── users.json          # User data
├── manage.py           # Django management script
```

#### Course
ENCE 420 - Software Engineering

#### Assignment Goals
>Students will design and implement a Python-based Online Library Management System (LMS) that supports user authentication, book copies management, and specialized functionality for Students and Teachers. They will also practice Agile development by implementing the system in Sprints and creating UML diagrams (Class, Use Case, Sequence).

##### Note: The specialized functionality for the different user roles was not used/implemented in the UI, but the functions exist in the class definitions within `models.py`
