from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('webcam/', views.webcam_feed, name='webcam_feed'),
    path('capture-image/', views.capture_image, name='capture_image'),
    path('upload-image/', views.upload_image, name='upload_image'),
    # path('login/', views.login_view, name='login'),
    path('login/', views.loginform, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


