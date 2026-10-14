from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    established = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


    
class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    isbn = models.CharField(max_length=13, unique=True,help_text="The book's unique ISBN number.")
    publication_date = models.DateField()
    genre_choices = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Children', 'Children'),
        ('Classic', 'Classic'),
        ('African Literature', 'African Literature'),
        ('Adventure', 'Adventure'),
        ('Science', 'Science'),
        ('Biology', 'Biology'),
        ('Finance', 'Finance'),
        ('Programming', 'Programming')
    ]
    genre = models.CharField(max_length=50, choices=genre_choices, default='Fiction')
    pages = models.IntegerField()
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5),], help_text="Rate this book from 0 to 5 stars.")
    summary = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    borrowed_count = models.IntegerField(default=0)
    language = models.CharField(max_length=50, default='English')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def full_title(self):
        if self.subtitle:
            return f"{self.title}: {self.subtitle}"
        return self.title

    def is_recent(self):
        if not self.publication_date:
            return False

        return (timezone.now().date() - self.publication_date).days <= 1825

    