from django import forms
from django.core.exceptions import ValidationError

from .models import Song


def validar_mp3(archivo):
    if not archivo.name.lower().endswith(".mp3"):
        raise ValidationError("Solo se permiten archivos MP3.")


class SongAdminForm(forms.ModelForm):
    audio_file = forms.FileField(
        required=False,
        validators=[validar_mp3],
        label="Archivo MP3",
    )

    class Meta:
        model = Song
        fields = [
            "title",
            "artist",
            "audio_file",
        ]