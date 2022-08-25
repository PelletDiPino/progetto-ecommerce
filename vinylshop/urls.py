from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    re_path(r'^$|^/$|home/', home, name='homepage'),
    path("admin/", admin.site.urls),
    path('account/', include('account.urls'))
]
