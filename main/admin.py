from django.contrib import admin
from .models import Book, Publisher, Genre, Author

# Register your models here.

admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Author)

