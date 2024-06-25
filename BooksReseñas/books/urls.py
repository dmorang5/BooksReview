from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (BookListView, AddReviewView, ReviewListView, UpdateReviewView, DeleteReviewView,
                    BookDetailView, AuthorListView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView,
                    PublishingListView, PublishingCreateView, PublishingUpdateView, PublishingDeleteView,
                    BookDeleteView)

urlpatterns = [
     #lISTAR LIBROS
     path('', BookListView.as_view(), name='book_list'),
     path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
     #RESEÑAS
     path('add_review/<int:book_id>/', AddReviewView.as_view(), name='add_review'),
     path('review_list/',ReviewListView.as_view() ,name='review_list'),
     path('upt_review/<int:book_id>/',UpdateReviewView.as_view(), name='upt_review'),
     path('delete_review/<int:book_id>/', DeleteReviewView.as_view(), name='delete_review'),
     #AUTOR
     path('author_list/', AuthorListView.as_view(), name='author_list'),
     path('author_create/', AuthorCreateView.as_view(), name='author_create'),
     path('author_update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),
     path('author_delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),
     #PUBLISHING/EDITORIAL
     path('publisher_list/', PublishingListView.as_view(), name='publisher_list'),
    path('publisher_create/', PublishingCreateView.as_view(), name='publisher_create'),
    path('publisher_update/<int:pk>/', PublishingUpdateView.as_view(), name='publisher_update'),
    path('publisher_delete/<int:pk>/', PublishingDeleteView.as_view(), name='publisher_delete'),
     #LIBRO
    path('book_delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]