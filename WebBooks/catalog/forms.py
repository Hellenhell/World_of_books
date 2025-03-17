from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book, Author

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']

class AuthorModelForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

