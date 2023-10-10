from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'webcam'

urlpatterns = [
    path('', views.index, name='webcam'),
    path('video_feed', views.video_feed, name='video_feed'),
]

if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_ORG, document_root=settings.MEDIA_ORG_ROOT)