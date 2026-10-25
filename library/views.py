from django.core import paginator
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, query
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Book
from .forms import BookModelForm, BookSearchForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import BookModelForm, BookSearchForm
from .forms import RegisterForm




# Create your views here.
from .forms import BookModelForm, BookSearchForm
from .models import Author, Book



def book_list(request):
    # Display a searchable, filterable, paginated list of books.

    search_form = BookSearchForm(request.GET or None)

    books = Book.objects.select_related('author', 'publisher').all()

    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'title')

    # Define the allowed sorting options first.
    sort_mapping = {
        'title': 'title',
        'author': 'author__last_name',
        'publication_date': 'publication_date',
        'rating': 'rating',
        'pages': 'pages',
    }

    # Search books by title, author, or ISBN.
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(isbn__icontains=query)
        )

    # Filter books by genre.
    if genre:
        books = books.filter(genre=genre)

    # Sort books, using title as the default.
    books = books.order_by(
        sort_mapping.get(sort_by, 'title')
    )

    # Display 12 books per page.
    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': query,
        'genre': genre,
        'sort_by': sort_by,
        # Preserve filters across pagination links.
        'query_params': _params_without_page(request),
    }

    return render(request, 'library/book_list.html', context)



def book_detail(request, pk):

#Display detailed information about a single book, plus similar titles.

    book = get_object_or_404(
    Book.objects.select_related('author', 'publisher'),
    pk=pk
    )
    similar_books = Book.objects.filter(
    genre=book.genre
    ).exclude(pk=book.pk).order_by('-rating')[:4]
    context = {
    'book': book,
    'similar_books': similar_books,
    }
    return render(request, 'library/book_detail.html', context)


@login_required
@permission_required('library.add_book', raise_exception=True)

def book_create(request):
    if request.method == 'POST':
        form = BookModelForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('book-list')

    else:
        form = BookModelForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'library/book_form.html',
        context
    )


@login_required
@permission_required('library.change_book', raise_exception=True)
def book_update(request, pk):
    # Get the existing book
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # Receive the submitted changes
        form = BookModelForm(
            request.POST,
            request.FILES,
            instance=book,
            user=request.user
        )

        # Check whether the submitted information is valid
        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'"{book.title}" was updated successfully.'
            )

            return redirect('library:book-detail', pk=book.pk)

        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:
        # Display the existing book details
        form = BookModelForm(
            instance=book,
            user=request.user
        )

    return render(request, 'library/book_form.html', {
        'form': form,
        'book': book,
        'title': f'Edit "{book.title}"',
        'submit_text': 'Save Changes',
    })


@login_required
@permission_required('library.delete_book', raise_exception=True)
def book_delete(request, pk):
    # Get the book or return a 404 error
    book = get_object_or_404(Book, pk=pk)

    # Check if the user has permission to delete the book
    if hasattr(book, 'created_by'):
        if not request.user.is_staff and book.created_by != request.user:
            raise PermissionDenied(
                "You don't have permission to delete this book."
            )

    # Delete the book only when the form is submitted
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(
            request,
            f'"{title}" was removed from the library.'
        )
        return redirect('library:book-list')

    # Show the confirmation page for GET requests
    return render(
        request,
        'library/book_confirm_delete.html',
        {'book': book}
    )


def book_search_ajax(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    books = Book.objects.filter(
    Q(title__icontains=query) | Q(author__last_name__icontains=query)
    ).select_related('author')[:10]
    results = [
        {'id': b.id, 'title': b.title, 'author': str(b.author)}
    for b in books
    ]
    return JsonResponse({'results': results})
@require_POST
@login_required
def book_toggle_availability(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_available = not book.is_available
    book.save(update_fields=['is_available'])
    return JsonResponse({'success': True, 'is_available': book.is_available})
def _params_without_page(request):
#Return the current GET querystring with 'page' stripped out."""
    params = request.GET.copy()
    params.pop('page', None)
    return params.urlencode()

def register(request):
    if request.user.is_authenticated:
        return redirect('library:book-list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            member_group, created = Group.objects.get_or_create(
                name='Member'
            )
            user.groups.add(member_group)

            login(request, user)

            messages.success(
                request,
                f'Welcome, {user.username}!'
            )

            return redirect('library:book-list')

    else:
        form = RegisterForm()

    return render(
        request,
        'library/register.html',
        {'form': form}
    )


@login_required
def profile(request):
    return render(request, 'library/profile.html')
