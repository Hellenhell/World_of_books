from django.contrib import admin

# Register your models here.

from .models import Author, Book, Genre, Language, Status, BookInstance

# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display =('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInline]

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('book', 'status')
    fieldsets = (('Экземпляр книги', {'fields': ('book', 'imprint', 'inv_nom')}), ('Статус и окончание его действия', {'fields': ('status', 'due_back', 'borrower')}),)
