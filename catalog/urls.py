from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('added_products/', views.AddedProductsView.as_view(), name='added_products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_details'),
    path('category/<int:category_id>/', views.ProductsByCategoryView.as_view(), name='products_by_category'),
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
]
