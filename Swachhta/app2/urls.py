from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('webcam/', views.webcam_feed, name='webcam_feed'),
    path('capture/', views.capture_image, name='capture_image'),
    # path('login/', views.login_view, name='login'),
    path('login/', views.loginform, name='login'),
    
]
