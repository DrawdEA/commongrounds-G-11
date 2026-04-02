from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


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
    

class BookReview(models.model):
    #userReviewer, foreign key to profile, cascade deletion, set upon login
    user_reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)

    #anonReviewer, text, set when not logged in
    anon_reviwer = models.TextField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    title = models.CharField()
    comment = models.TextField()

    def __str__(self):
        return self.title 

class Bookmark(models.model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField()

    def __str__(self):
        return self

class Borrow(models.model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    #borrower, foreignkey to profile, cascading deletion, set upon login
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE)

    #name, characterfield, set when not logged in
    name = models.CharField()

    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        return self

