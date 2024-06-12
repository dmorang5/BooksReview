from django.contrib import admin
from .models import Author, Publishing, Book, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Publishing)
class PublishingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publishing', 'year')
    list_filter = ('author', 'publishing', 'year')
    search_fields = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'pub_date', 'user', 'comment', 'rating')
    list_filter = ('book', 'pub_date', 'user')
