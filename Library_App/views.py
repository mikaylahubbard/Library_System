from django.shortcuts import render, redirect
from .models import *
from .models import Library, Student, Teacher
from django.contrib import messages

library = Library()



# library.add_book(Book("Serious Cryptography", "Aumasson", "technology", 4, 4))
# library.add_book(Book("Frankenstein", "Mary Shelley", "english", 3, 3))

# Create your views here.
def home(request):
    # always refresh from disk
    library.users = []
    library.books = []
    library.passwords = {}

    library._load_users()
    library._load_books()

    user_id = request.session.get("user_id")
    user = None
    borrowed_books = []
    
    # Handle logout action
    if request.method == "POST" and "logout" in request.POST:
        request.session.flush()  # clear session safely
        return redirect("/")

    if user_id:
        for u in library.users:
            if u.user_id == user_id:
                user = u
                break
            
    if request.method == "POST" and "borrow" in request.POST:
        book_id = request.POST.get("book_id")
        if user:
            # Find book
            book_id = request.POST.get("book_id")
            print("POST book_id:", repr(request.POST.get("book_id")))
            print("Library book_ids:", [str(b.book_id) for b in library.books])
            book = next((b for b in library.books if b.book_id == book_id), None)
            user.borrow_book(book)

            # Save library after borrowing
            library._save_users()
            library._save_books()

        return redirect('/')  
    if user:
            # resolve book IDs into actual Book objects
            borrowed_books = [
                b for b in library.books if b.book_id in user.borrowed_books
            ]
            
    
    return render(request, "home.html", {"user": user, "books": library.books, "borrowed_books": borrowed_books})

def login_page(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        print("POST user_id:", repr(user_id))
        print("POST password:", repr(password))
        user = library.authenticate(user_id, password)
        if user:
            request.session["user_id"] = user.user_id
            return redirect('/')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
    return render(request, "login.html")


def register_page(request):
    request.session.flush()  # clear session safely
    if request.method == "POST":
        user_id = request.POST["user_id"]
        f_name = request.POST["f_name"]
        l_name = request.POST["l_name"]
        password = request.POST["password"]
        role = request.POST["role"]
        subject = request.POST["subject"]
        

        if role == "student":
            user = Student(user_id, f_name, l_name, password, subject)
        else:
            user = Teacher(user_id, f_name, l_name, password, subject)

        library.register_user(user)
        return redirect('/login/')

    return render(request, "register.html")