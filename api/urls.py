from django.urls import path
from . import views

urlpatterns = [
    path('api_spec/', views.ApiSpec.as_view()),
    path('import/', views.ImportBooks.as_view()),
    path('books/', views.Books.as_view()),
    path('books/<str:pk>', views.BookDetail.as_view()),
]