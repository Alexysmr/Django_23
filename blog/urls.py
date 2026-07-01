from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogView.as_view(), name='index'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='details'),
    path('edit/<int:pk>/', views.PostEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete'),
    ]