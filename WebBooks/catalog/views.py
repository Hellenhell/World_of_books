from .models import Book, Author, BookInstance
from django.shortcuts import render, redirect
from django.http import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=1).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html', context={'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available, 'num_authors': num_authors, 'num_visits': num_visits})

def no_permission(request):
    return render(request, 'no_permission.html')
 
class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')

class RedirectPermissionRequiredMixin(PermissionRequiredMixin,):
    login_url = reverse_lazy('no_permission')

    def handle_no_permission(self):
        return redirect(self.get_login_url())

class BookCreate(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    permission_required = 'WebBooks.add_Book'
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    permission_required = 'WebBooks.change_Book'
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(LoginRequiredMixin, RedirectPermissionRequiredMixin, DeleteView):
    permission_required = 'WebBooks.delete_Book'
    model = Book
    success_url = reverse_lazy('books')

class AuthorCreate(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    permission_required = 'WebBooks.add_Author'
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')

class AuthorUpdate(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    permission_required = 'WebBooks.change_Author'
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')

class AuthorDelete(LoginRequiredMixin, RedirectPermissionRequiredMixin, DeleteView):
    permission_required = 'WebBooks.delete_Author'
    model = Author
    success_url = reverse_lazy('authors')

def order(request, id):
    try:
        book_instance = BookInstance.objects.get(id=id)
        book_instance.status_id = 2
        book_instance.borrower_id = request.user.id
        book_instance.save(update_fields=["status_id", "borrower_id",])
    except BookInstance.DoesNotExist:
        raise Http404
    return HttpResponseRedirect("/books/")

