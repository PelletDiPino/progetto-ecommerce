from django.urls import path
from .views import *
from product.views import CreateProduct, ProductsListView

app_name = 'product'

urlpatterns = [
    path('create_product/', CreateProduct.as_view(), name='create_product'),
    path('list_product/', ProductsListView.as_view(), name='list_products'),
]
