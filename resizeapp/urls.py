from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_resize_image, name='upload_and_resize_image'),
    path('upload-image-file/', views.upload_image_file, name='upload_image_file'),  # URL for Dropzone.js
]
