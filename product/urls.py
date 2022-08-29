from django.urls import path
from .views import *
from product.views import CreateProduct, ProductsListView, ProductDetails, VendorDetails, productReview

app_name = 'product'

urlpatterns = [
    path('create_product/', CreateProduct.as_view(), name='create_product'),
    path('list_product/', ProductsListView.as_view(), name='list_products'),
    path('<slug:slug>/details', ProductDetails.as_view(), name='product_details'),
    path('vendor_details/<int:pk>/', VendorDetails.as_view(), name='vendor_details'),
    path('<slug:slug>/review', productReview, name='product_review'),
    path('<int:pk>/vendor_review', vendorReview, name='vendor_review')
]
