from django.urls import path
from . import views

urlpatterns = [
    path("songs/<uuid:uuid>/", views.SongDetailView.as_view(), name="song-detail"), 
]
