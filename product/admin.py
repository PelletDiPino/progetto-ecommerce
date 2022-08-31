from django.contrib import admin
from .models import Category, Product, ProductReview, VendorReview, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(VendorReview)
admin.site.register(Order)