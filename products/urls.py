from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<slug:category_slug>/', views.all_products, name='products_by_category'),
]
