from django.shortcuts import render, redirect, get_object_or_404

from .forms import *


# Create your views here.

def index(request):
    if request.method == 'POST':
        new_book = BookForm(request.POST, request.FILES)
        if new_book.is_valid():
            new_book.save()

        new_category = CategoryForm(request.POST)
        if new_category.is_valid():
            new_category.save()

    context = {
        'categories': CategoryModel.objects.all(),
        'books': BookModel.objects.all(),
        'books_form': BookForm(),
        'categories_form': CategoryForm(),
        'all_books': BookModel.objects.filter(active=True).count(),
        'book_sold': BookModel.objects.filter(status='sold').count(),
        'book_rental': BookModel.objects.filter(status='rental').count(),
        'book_available': BookModel.objects.filter(status='available').count(),
    }
    return render(request, 'pages/index.html', context=context)


def books_view(request):
    books = BookModel.objects.all()
    if 'search_name' in request.GET and request.GET['search_name']:
        books = books.filter(title__icontains=request.GET['search_name'])
    context = {
        'categories': CategoryModel.objects.all(),
        'books': books,
        'books_form': BookForm(),
        'categories_form': CategoryForm(),
    }
    return render(request, 'pages/books.html', context=context)


def update(request, id):
    book = BookModel.objects.get(id=id)
    if request.method == 'POST':
        update_book = BookForm(request.POST, request.FILES, instance=book)
        if update_book.is_valid():
            update_book.save()
            return redirect('/')
    else:
        update_book = BookForm(instance=book)

    context = {
        'book_form': update_book,
    }
    return render(request, 'pages/update.html', context=context)


def delete(request, id):
    book = get_object_or_404(BookModel, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('/')
    return render(request, 'pages/delete.html')
