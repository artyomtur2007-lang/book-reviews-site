from django.core.paginator import Paginator
from django.shortcuts import render

from .filters import ContentFilter
from .models import Book, Review

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ReviewForm

from django.shortcuts import redirect
from .forms import BookForm

@login_required
def add_book_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'core/add_review.html', {
        'form': form,
        'book': book
    })

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'core/book_detail.html', context)

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'core/add_book.html', {
        'form': form
    })

ITEMS_PER_PAGE = 50


def home_page(request):
    top_books = Book.objects.order_by('-average_rating')[:10]
    recent_reviews = Review.objects.order_by('-created_at')[:10]

    context = {
        'top_books': top_books,
        'recent_reviews': recent_reviews,
        'total_books': Book.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    return render(request, 'core/home.html', context)


def book_list(request):
    f = ContentFilter(request.GET, queryset=Book.objects.all())

    sort_param = request.GET.get('sort', '-average_rating')

    if sort_param == 'rating':
        books_qs = f.qs.order_by('-average_rating')
    elif sort_param == '-rating':
        books_qs = f.qs.order_by('average_rating')
    else:
        books_qs = f.qs.order_by(sort_param)

    paginator = Paginator(books_qs, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': f,
        'page_obj': page_obj,
        'current_sort': sort_param,
        'query_params': request.GET.urlencode(),
        'sort_desc_rating': sort_param == '-average_rating',
        'sort_asc_rating': sort_param == 'average_rating',
        'sort_newest': sort_param == '-id',
        'sort_title': sort_param == 'title',
    }

    if request.htmx:
        return render(request, 'core/partials/book_list_content.html', context)

    return render(request, 'core/book_list.html', context)