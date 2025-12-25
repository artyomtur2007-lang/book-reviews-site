from django.contrib import admin
from .models import Genre, Book, Movie, Review

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Movie)
admin.site.register(Review)

