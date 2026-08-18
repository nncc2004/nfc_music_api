from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from .models import Song
from .serializers import SongSerializer


class SongDetailView(RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = "uuid"