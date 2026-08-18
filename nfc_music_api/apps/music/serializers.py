from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    audio_url = serializers.URLField(
        source="firebase_url",
        read_only=True,
    )

    class Meta:
        model = Song
        fields = (
            "uuid",
            "title",
            "artist",
            "audio_url",
        )