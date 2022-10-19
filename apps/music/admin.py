from django.contrib import admin

from .models import Album, Artist, Genre, Playlist, RecordLabel, Song, SongPlayLog


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "artist")
    list_select_related = ("artist",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_select_related = ("artist", "album")
    list_display = ("name", "artist", "time_length")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["user", "name"]
    list_select_related = ("user",)

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(SongPlayLog)
class SongPlayLogAdmin(admin.ModelAdmin):
    list_display = ["user", "song", "date_played"]
    list_select_related = ("user", "song")
