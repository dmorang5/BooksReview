from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Author, Publishing, Book, Review
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm, AuthorForm, PublisherForm, BookForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import MultipleObjectsReturned
from django.contrib import messages

def is_admin(user):
    return user.is_superuser

# Vistas para Author
@method_decorator(login_required, name='dispatch')
class AuthorListView(ListView):
    model = Author
    template_name = 'author/author_list.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorForm()
        context['update_form'] = AuthorForm()
        return context

    def post(self, request, *args, **kwargs):
        author_id = request.POST.get('author_id')
        if author_id:
            author = get_object_or_404(Author, pk=author_id)
            form = AuthorForm(request.POST, request.FILES, instance=author)
        else:
            form = AuthorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('author_list')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AuthorCreateView(CreateView):
    model = Author
    template_name = 'author/author_form.html'
    fields = ['name', 'description', 'cover_image']

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'author/author_form.html'
    fields = ['name', 'description', 'cover_image']

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')

# Vistas para Publishing (editorial)
@method_decorator(login_required, name='dispatch')
class PublishingListView(ListView):
    model = Publishing
    template_name = 'publishing/publishing_list.html'
    context_object_name = 'publishers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PublisherForm()
        context['update_form'] = PublisherForm()
        return context

    def post(self, request, *args, **kwargs):
        publisher_id = request.POST.get('publisher_id')
        if publisher_id:
            publisher = get_object_or_404(Publishing, pk=publisher_id)
            form = PublisherForm(request.POST, request.FILES, instance=publisher)
        else:
            form = PublisherForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('publisher_list')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class PublishingCreateView(CreateView):
    model = Publishing
    template_name = 'publishing/publishing_form.html'
    fields = ['name', 'description', 'logo']

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class PublishingUpdateView(UpdateView):
    model = Publishing
    template_name = 'publishing/publishing_form.html'
    fields = ['name', 'description', 'logo']

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class PublishingDeleteView(DeleteView):
    model = Publishing
    template_name = 'publishing/publishing_confirm_delete.html'
    success_url = reverse_lazy('publisher_list')

# Vistas para Book
@method_decorator(login_required, name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    ordering = ['-year']  # Ordenar los libros por año descendente

    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        return context

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        if book_id:
            book = get_object_or_404(Book, pk=book_id)
            form = BookForm(request.POST, request.FILES, instance=book)
        else:
            form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            if 'year' in form.cleaned_data and form.cleaned_data['year']:
                book.year = form.cleaned_data['year'].replace(month=1, day=1)
            else:
                book.year = timezone.now().replace(month=1, day=1)

            # Verificar si se ha proporcionado un archivo para cover_libro
            if 'cover_libro' in request.FILES:
                book.cover_libro = request.FILES['cover_libro']
            book.save()
            return redirect('book_list')

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

@login_required
@user_passes_test(is_admin)
class BookCreateView(CreateView):
    model = Book
    template_name = 'book/book_form.html'
    fields = ['title', 'synopsis', 'year', 'author', 'publishing', 'cover_libro']

@login_required
@user_passes_test(is_admin)
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book/book_form.html'
    fields = ['title', 'synopsis', 'year', 'author', 'publishing', 'cover_libro']


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')


# VISTA RESEÑAS
class AddReviewView(FormView):
    template_name = 'Review/add_review.html'
    form_class = ReviewForm

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        user = self.request.user

        if Review.objects.filter(book_id=book_id, user=user).exists():
            messages.error(self.request, "Ya haz reseñado este libro.")
            return self.form_invalid(form)

        book = get_object_or_404(Book, id=book_id)
        review = form.save(commit=False)
        review.user = self.request.user
        review.book = book
        review.pub_date = timezone.now()
        review.save()
        return redirect('book_list')

class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'Review/add_review.html'

    def get_object(self, queryset=None):
        book_id = self.kwargs['book_id']
        user = self.request.user
        try:
            return Review.objects.get(book_id=book_id, user=user)
        except MultipleObjectsReturned:
            # Manejar el caso donde hay múltiples revisiones
            return Review.objects.filter(book_id=book_id, user=user).first()

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.pub_date = timezone.now()
        review.save()
        return redirect('review_list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('review_list')

@method_decorator(login_required, name='dispatch')
class ReviewListView(ListView):
    model = Review
    template_name = 'Review/review_list.html'
    context_object_name = 'review'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'Review/confirm_delete.html'
    context_object_name = 'review'

    def get_object(self, queryset=None):
        book_id = self.kwargs['book_id']
        return get_object_or_404(Review, book_id=book_id, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('review_list')

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = Review.objects.filter(book=self.object)
        context['average_rating'] = book.average_rating()
        return context
