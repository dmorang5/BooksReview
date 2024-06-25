from crum import get_current_user

from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.utils import timezone
from models import BaseModel
class Author(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='author/covers/', blank=True, null=True)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        if not self.cover_image:
            self.cover_image = 'author/covers/default_cover.jpg'  # Ruta de la imagen por defecto
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Publishing(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='publisher_logos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        if not self.logo:
            self.logo = 'publisher_logos/default_logo.jpg'  # Ruta de la imagen por defecto
        super(Publishing, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(BaseModel):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    year = models.DateField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publishing = models.ForeignKey(Publishing, on_delete=models.CASCADE)
    cover_libro = models.ImageField(upload_to='books/', blank=True, null=True)

    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        if not self.cover_libro:
            self.cover_image = 'books/default_cover.jpg'  # Ruta de la imagen por defecto
        super(Book, self).save(*args, **kwargs)

    def rating_stars(self):
        rating = self.average_rating()
        if rating is not None:
            full_stars = int(rating)
            half_stars = round(rating - full_stars)
            empty_stars = 5 - full_stars - half_stars
            stars = "★" * full_stars + "½" * half_stars + "☆" * empty_stars
            return stars
        return ''

    def __str__(self):
        return f'{self.title} {self.year}'

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
