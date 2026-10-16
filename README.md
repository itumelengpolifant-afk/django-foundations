#Django Foundations - Library Management System

A library website built with Python and Django. Books, authors and publishers are stored in a database and managed through web pages, with search, filtering, sorting and pagination features. 

##Technologies and Versions
 - Python  | 3.14.6
 - Django  | 6.1.1
 - Pillow  |12.3.0
 - asgiref / sqlparse / tzdata | 3.12.1 / 0.6.0 / 2026.4|
 - Database | SQLite3
 - Front end | HTML, CSS, Django Template Language|
 - Tools   | Git, GitHub, Visual Studio Code |

 ##What I Built, Start to finish
 1. Created a virtual environment, installed Django and started the project
 2. Before I started my project I created a branch to my GitHub and named it "library"
 3. Created the 'library' app and registered it in 'INSTALLED APPS'
 4. Built the 'Author', 'Publisher' and 'Book' models, linking each book to it's author and publisher with foreign keys.
 5. Ran migrations to create the SQLite database tables 
 6. Wrote function-based views, URL patterns and templates to list books and show book details.
 7. Built an add-book form 'BookModelForm' with validation
 8. Added genre filtering, search, sorting and pagination to the book list.
 9. Fixed errors along the way and tracked all changes with Git and GitHub on the 'library' branch


 # Run it Locally
 ```
 git clone YOUR_GITHUB_REPOSITORY_URL
 cd django-foundations
 python -m venv myvenv
 source myvenv/Scripts/activate
 python -m pip install -r requirements.txt
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver
 ```

 Then open http://127.0.0.1:8000/books/