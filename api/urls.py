from django.urls import path
from . import views

urlpatterns = [
    path('api_spec/', views.ApiSpec.as_view()),
    path('import/', views.ImportBooks.as_view(), name='import'),
    path('books/', views.Books.as_view(), name='book_list'),
    path('books/<str:pk>', views.BookDetail.as_view(), name='book_detail'),
]