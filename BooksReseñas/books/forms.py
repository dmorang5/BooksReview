from django import forms
from .models import Review, Author, Publishing, Book
from django.utils import timezone


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'book' in kwargs:
            self.fields['book'].widget = forms.HiddenInput()

    def get_initial(self):
        initial = super().get_initial()
        if 'book' in self.initial:
            initial['book'] = self.initial['book']
        return initial

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'description', 'cover_image']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publishing
        fields = ['name', 'description', 'logo']

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'synopsis', 'year', 'author', 'publishing', 'cover_libro']
        widgets = {
            'year': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer la fecha actual por defecto para el campo year
        self.fields['year'].initial = timezone.now().date()
