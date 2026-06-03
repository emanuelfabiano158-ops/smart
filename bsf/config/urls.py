from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('smart/', admin.site.urls),
    path('', include('wlas.urls')),  # connects your app
]


