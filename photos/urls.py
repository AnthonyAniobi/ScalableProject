from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload/', views.upload_photo, name='upload'),
    path('photo/<int:photo_id>/', views.photo_detail, name='detail'),
    path('photo/<int:photo_id>/like/', views.toggle_like, name='toggle_like'),
    path('photo/<int:photo_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
]