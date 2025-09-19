from django.db import models
import random
import os
import json

# Create your models here.


class Book:
    def __init__(self, id, title, author, subject, total_copies, available_copies):
        self.book_id = id
        self.title = title
        self.author = author
        self.subject = subject
        
        self.total_copies: int = total_copies
        self.available_copies: int = available_copies
        self.available: bool = self.check_availability()
        
    def check_availability(self):
        if (self.available_copies > 0):
            return True
        else:
            return False
    
    def update_return(self):
        if (self.available_copies < self.total_copies):
            self.available_copies += 1

    def update_borrow(self):
        if (self.available_copies > 0):
            self.available_copies -= 1;    


class User:
    def __init__(self, id, f_name, l_name, password, subject):
        self.user_id = id
        self.f_name = f_name
        self.l_name = l_name
        self.password = password
        self.subject = subject
        self.borrowed_books = []
        
    def borrow_book(self, book: Book) -> bool:
        if (book.available_copies >= 1):
            self.borrowed_books.append(book)
            book.update_borrow()
            # successfully borrowed 
            return True
        else:
            # book is unavailable
            return False
        
    def return_book(self, book: Book):
        book.update_return()
        self.borrowed_books.remove(book)
        # successfully returned
        


class Student(User):
    def __init__(self, id, f_name, l_name, password, subject):
        super().__init__(id, f_name, l_name, password, subject)
        
    def view_grades(self):
        # This is a static result - we do not have a grades feature
        grades = [84, 93, 75, 90, 86]
        return grades
    
    def request_rec(self):
        options = []
        for b in Library.books:
            if b.subject == self.subject:
                options.append(b)
        if options != []:
            rec = random.choice(options)
            return rec
        else:
            return "No Matching Books"
        
        
        
    
class Teacher(User):
    def __init__(self, id, f_name, l_name, password, subject):
       super().__init__(id, f_name, l_name, password, subject)
       
    def add_material(book: Book):
        Library.books.append(book)
       
    def review_borrowed_books(self):
        borrowed_books = {}
        for b in Library.books:
            # to find the number of borrowed: total - available
            num_borrowed = b.total_copies - b.available_copies
            borrowed_books[b.book_id] = num_borrowed
        return borrowed_books
            
        
    

class Library:
    def __init__(self):
        self.books =  []
        self.users =  []
        self.passwords = {}
        self.users_file = "Library_App/users.json"
        self.books_file = "Library_App/books.json"
        
        self._load_users()
        self._load_books()
        
        
        print("Passwords:", self.passwords)
        print("Users:", [u.user_id for u in self.users])
        
    def add_book(self, book: Book):
        print("book was added")
        self.books.append(book)
        self._save_books()
        print(f"Book '{book.title}' added to library.")
    
    def remove_book(self, book: Book):
        removed = self.books.pop(book)
        self._save_books()
        print(f"Book '{removed.title}' removed from library.")

    def register_user(self, user: User):
            self.users.append(user)
            self.passwords[user.user_id] = user.password
            self._save_users()
            print(f"User '{user.f_name}' registered.")

    def authenticate(self, user_id: str, password: str):
        print("Trying to login:", user_id, password)
        print("Known passwords:", self.passwords)
        if user_id in self.passwords and self.passwords[user_id] == password:
            print("Password in JSON:", self.passwords[user_id])
            # find the actual user object
            for u in self.users:
                if u.user_id == user_id:
                    return u
        return None
        # if user_id in self.passwords and self.passwords[user_id] == password:
        #     print("Login successful")
        #     return self.users[user_id]
        # else:
        #     print("Login failed")
        #     return None

    def search_book(self, title):
        results = [book for book in self.books.values() if title.lower() in book.title.lower()]
        return results    
    
    def _load_users(self):
        """Load users from JSON file if it exists."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                data = json.load(f)
                for u in data:
                    if u["role"] == "student":
                        user = Student(u["user_id"], u["f_name"], u["l_name"], u["password"], u["subject"])
                    else:
                        user = Teacher(u["user_id"], u["f_name"], u["l_name"], u["password"], u["subject"])
                    self.users.append(user)
                    self.passwords[user.user_id] = user.password

    def _save_users(self):
        """Save users to JSON file."""
        data = []
        for user in self.users:
            role = "student" if isinstance(user, Student) else "teacher"
            data.append({
                "user_id": user.user_id,
                "f_name": user.f_name,
                "l_name": user.l_name,
                "password": user.password,   # normally hash this
                "subject": user.subject,
                "role": role,
                "borrowed_books": user.borrowed_books
            })
        with open(self.users_file, "w") as f:
            json.dump(data, f, indent=4)
            
    def _load_books(self):
        if os.path.exists(self.books_file):
            with open(self.books_file, "r") as f:
                data = json.load(f)
                for b in data:
            
                    book = Book(b["book_id"], b["title"], b["author"], b["subject"], b["total_copies"], b["available_copies"])
                    self.books.append(book)
                    
    
    def _save_books(self):
        data = []
        for book in self.books:
            data.append({
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "total_copies": book.total_copies,
                "available_copies": book.available_copies,
                "available": book.available
            })
        with open(self.books_file, "w") as f:
            json.dump(data,f, indent=4)
     


    