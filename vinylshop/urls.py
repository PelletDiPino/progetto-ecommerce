from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^$|^/$|home/', home, name='homepage'),
    path("admin/", admin.site.urls),
    path("account/", include('account.urls')),
    path("product/",include('product.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
