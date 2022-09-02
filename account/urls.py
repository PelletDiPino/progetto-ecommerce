from django.urls import path
from .views import UserCreateView, UserLogin, UserLogout, MySales, MySalesDetails, AccountDetails, AccountVendorDetails
from product.views import ProductUpdate

app_name = 'account'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name="register"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('mysales/', MySales.as_view(), name="my_sales"),
    path('mysales/<slug:slug>/detail', MySalesDetails.as_view(), name="sale_detail"),
    path('mysales/<slug:slug>/update', ProductUpdate.as_view(), name="product_update"),
    path('info', AccountDetails.as_view(), name='account_details'),
    path('vendor_info', AccountVendorDetails.as_view(), name='account_vendor_details'),
]
