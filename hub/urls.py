from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'hub'

urlpatterns = [
    path('', cache_page(60 * 60 * 12)(views.HubView.as_view()), name='hub'),
]