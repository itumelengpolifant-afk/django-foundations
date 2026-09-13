from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world(request):
    html = """
        <html>
        <head>
        <title>Hello, World!</title>
        </head>
        <body>
        <h1 style="color: pink;">Hello, World!</h1>
        <p>Welcome to Django!</p>
        </body>
        </html>
    """
    return HttpResponse(html)
