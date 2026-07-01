from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.HubView.as_view(), name='hub'),
]