from django.contrib import admin

from .models import Song
from .forms import SongAdminForm
from apps.firebase.utils import (
    subir_archivo_firebase,
    eliminar_archivo_firebase,
)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = SongAdminForm

    list_display = (
        "title",
        "artist",
        "uuid",
        "uploaded_by",
        "firebase_url",
        "created_at",
    )

    list_display_links = ("title",)

    search_fields = (
        "title",
        "artist",
        "uuid",
        "uploaded_by__username",
        "uploaded_by__email",
    )

    list_filter = (
        "artist",
        "uploaded_by",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "uuid",
        "firebase_url",
        "uploaded_by",
        "created_at",
    )

    fields = (
        "uuid",
        "title",
        "artist",
        "audio_file",
        "firebase_url",
        "uploaded_by",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user

        archivo = form.cleaned_data.get("audio_file")

        if archivo:
            if change and obj.firebase_url:
                eliminar_archivo_firebase(obj.firebase_url)

            nueva_url = subir_archivo_firebase(archivo)

            if nueva_url:
                obj.firebase_url = nueva_url

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Elimina el archivo de Firebase al eliminar una canción."""

        if obj.firebase_url:
            eliminar_archivo_firebase(obj.firebase_url)

        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """Elimina los archivos de Firebase antes de eliminar los registros."""

        for obj in queryset:
            if obj.firebase_url:
                eliminar_archivo_firebase(obj.firebase_url)

        queryset.delete()