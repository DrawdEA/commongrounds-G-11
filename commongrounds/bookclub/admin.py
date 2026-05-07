from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_year', 'available_to_borrow')
    list_filter = ('genre', 'available_to_borrow')

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'user_reviewer', 'anon_reviewer')

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'book', 'date_bookmarked')

class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'name', 'borrower', 'date_borrowed', 'date_to_return')

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Borrow, BorrowAdmin)