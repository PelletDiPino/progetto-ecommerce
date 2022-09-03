from django.urls import path

from product.views import CreateProduct, ProductsListView, ProductDetails, \
    VendorDetails, product_review, vendor_review, ProductDelete, BuyProduct, add_order, \
    search, search_price, CategoryListView, category_filter_view

app_name = 'product'

urlpatterns = [
    path('create_product/', CreateProduct.as_view(), name='create_product'),
    path('<slug:slug>/delete', ProductDelete.as_view(), name='delete_product'),
    path('list_product/', ProductsListView.as_view(), name='list_products'),
    path('categories_list/', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/list', category_filter_view, name='category_filter'),
    path('<slug:slug>/details', ProductDetails.as_view(), name='product_details'),
    path('<slug:slug>/buy', BuyProduct.as_view(), name='product_buy'),
    path('vendor_details/<int:pk>/', VendorDetails.as_view(), name='vendor_details'),
    path('<slug:slug>/review', product_review, name='product_review'),
    path('<int:pk>/vendor_review', vendor_review, name='vendor_review'),
    path('<slug:slug>/add_order', add_order, name="add_order"),
    path('search/', search, name="search"),
    path('price_search/', search_price, name="price_search"),
]
