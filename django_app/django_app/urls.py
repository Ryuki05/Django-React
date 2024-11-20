from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',include('hello.urls')),
    path('sns/',include('sns.urls')),
    path('api/', include('api.urls')),
]
