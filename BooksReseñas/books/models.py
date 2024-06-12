from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='author/covers/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.cover_image:
            self.cover_image = 'author/covers/default_cover.jpg'  # Ruta de la imagen por defecto
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Publishing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='publisher_logos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.logo:
            self.logo = 'publisher_logos/default_logo.jpg'  # Ruta de la imagen por defecto
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    year = models.DateField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publishing = models.ForeignKey(Publishing, on_delete=models.CASCADE)
    cover_libro = models.ImageField(upload_to='books/', blank=True, null=True)

    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def save(self, *args, **kwargs):
        if not self.cover_libro:
            self.cover_libro = 'books/default_cover.jpg'  # Ruta de la imagen por defecto
        super().save(*args, **kwargs)

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
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)