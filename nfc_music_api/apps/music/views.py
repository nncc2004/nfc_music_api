'''
from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from .models import Song
from .serializers import SongSerializer


class SongDetailView(RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = "uuid"
'''

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Song
from .serializers import SongSerializer


class SongDetailView(RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        try:
            song = self.get_object()
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not song.firebase_url:
            return Response(
                {"error": "Audio file not available"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(song)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )