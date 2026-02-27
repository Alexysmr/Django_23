from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('answer_by_message/', views.contact_success, name='contact_success'),
    path('added_products/', views.added_products, name='added_products'),
    path('product/<int:pk>/', views.product_details, name='product_details'),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('add-product/', views.add_product, name='add_product'),
]
