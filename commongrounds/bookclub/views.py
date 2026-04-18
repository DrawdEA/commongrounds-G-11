import datetime
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book, Bookmark, BookReview
from .forms import BookForm, BookReviewForm, BorrowForm

class ContributorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.has_perm('bookclub.add_book')
        return False


class BookListView(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'all_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_qs = Book.objects.all()

        # If logged in and has a profile, split the lists
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            
            contributed = all_books_qs.filter(contributor=profile)
            user_bookmarked_ids = Bookmark.objects.filter(profile=profile).values_list('book_id', flat=True)
            bookmarked = all_books_qs.filter(id__in=user_bookmarked_ids)
            reviewed = all_books_qs.filter(reviews__user_reviewer=profile)
            
            context['contributed_books'] = contributed
            context['bookmarked_books'] = bookmarked
            context['reviewed_books'] = reviewed
            
            # Remove the above books from the 'All Books' list
            context['all_books'] = all_books_qs.exclude(id__in=contributed).exclude(id__in=bookmarked).exclude(id__in=reviewed)
            
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'bookclub/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        
        # Add the review form and bookmark count to the context
        context['review_form'] = BookReviewForm()
        context['bookmark_count'] = book.bookmarks.count()
        context['reviews'] = book.reviews.all()
        
        # Check if current user is the contributor to show the Edit link
        context['is_contributor'] = False
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            if book.contributor == self.request.user.profile:
                context['is_contributor'] = True
                
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        
        if 'bookmark' in request.POST and request.user.is_authenticated and hasattr(request.user, 'profile'):
            Bookmark.objects.get_or_create(profile=request.user.profile, book=book)
            return redirect('bookclub:book_detail', pk=book.pk)
            
        review_form = BookReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = "Anonymous"
                
            review.save()
            return redirect('bookclub:book_detail', pk=book.pk)
            
        return self.get(request, *args, **kwargs)

class BookCreateView(LoginRequiredMixin, ContributorRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'
    success_url = reverse_lazy('bookclub:book_list')

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, ContributorRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'
    
    def get_success_url(self):
        return reverse_lazy('bookclub:book_detail', kwargs={'pk': self.object.pk})

class BookBorrowView(CreateView):
    form_class = BorrowForm
    template_name = 'bookclub/borrow_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            initial['name'] = self.request.user.profile.display_name
        return initial

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            form.instance.borrower = self.request.user.profile
            
        form.instance.date_to_return = form.instance.date_borrowed + datetime.timedelta(days=14)
        
        book.available_to_borrow = False
        book.save()
        
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('bookclub:book_detail', kwargs={'pk': self.kwargs['pk']})