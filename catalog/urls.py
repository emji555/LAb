from django.urls import path
from . import views
from .views import SearchResultsView


urlpatterns = [
    path('',views.index , name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(),name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('genres/',views.GenreListView.as_view(),name='gener'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
