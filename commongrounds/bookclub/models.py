from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name'] 

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    contributor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=255)
    synopsis = models.TextField()
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']
        
    def __str__(self):
        return self.title 
    

class BookReview(models.Model):
    #userReviewer, foreign key to profile, cascade deletion, set upon login
    user_reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    anon_reviewer = models.CharField(max_length=255, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"Review: {self.title} by {self.user_reviewer or self.anon_reviewer}"

class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookmarks')
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book}"

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        return f"{self.name or self.borrower} borrowed {self.book}"

