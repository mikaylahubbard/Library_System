from django.shortcuts import render, redirect
from .models import *
from .models import Library, Student, Teacher
from django.contrib import messages

library = Library()
# Create your views here.
def home(request):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        for u in library.users:
            if u.user_id == user_id:
                user = u
                break
    return render(request, "home.html", {"user": user})

def login_page(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        print("POST user_id:", repr(user_id))
        print("POST password:", repr(password))
        user = library.authenticate(user_id, password)
        print(user)
        if user:
            request.session["user_id"] = user.user_id
            return redirect('/')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
    return render(request, "login.html")

def logout_page(request):
    if request.method == "POST":
        del request.session["user_id"]
        return redirect("login")
    return render(request, 'logout.html')

def register_page(request):
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