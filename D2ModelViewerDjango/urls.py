from django.contrib import admin
from django.urls import path
from d2app import views

urlpatterns = [
    path('', views.index),
    path('submit', views.submit),
    path('admin/', admin.site.urls),
]
