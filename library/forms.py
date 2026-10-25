
from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookModelForm(forms.ModelForm):
    # Form for creating and updating Book instances.

    class Meta:
        model = Book
        fields = [
            'title', 'subtitle', 'author', 'publisher', 'isbn',
            'publication_date', 'genre', 'pages', 'summary',
            'cover_image', 'language', 'is_available', 'rating',
        ]

        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'summary': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

        labels = {
            'title': 'Book Title',
            'publication_date': 'Date Published',
        }

        help_texts = {
            'rating': 'Rate the book from 1 to 5.',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.HiddenInput):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (
                    existing + ' form-control'
                ).strip()

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and len(title) < 3:
            raise forms.ValidationError(
                'Title must be at least 3 characters.'
            )

        return title

    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn")

        if isbn and Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError(
                "A book with this ISBN already exists."
            )

        return isbn

class BookSearchForm(forms.Form):
    # Form for searching and filtering books.

    q = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or ISBN...',
        })
    )

    genre = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    sort = forms.ChoiceField(
        choices=[
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
            ('-rating', 'Highest Rated'),
            ('-publication_date', 'Newest'),
            ('publication_date', 'Oldest'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].choices = [
            ('', 'All Genres')
        ] + list(Book.genre_choices)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user




