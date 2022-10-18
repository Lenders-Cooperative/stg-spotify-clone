import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum  # noqa
from django.utils import timezone
from django.views.generic import TemplateView

User = get_user_model()
Profile = apps.get_model("users", "Profile")
Genre = apps.get_model("music", "Genre")
RecordLabel = apps.get_model("music", "RecordLabel")
Playlist = apps.get_model("music", "Playlist")
Album = apps.get_model("music", "Album")
Artist = apps.get_model("music", "Artist")
Song = apps.get_model("music", "Song")
City = apps.get_model("content", "City")
SongPlayLog = apps.get_model("music", "SongPlayLog")


class HomeView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "home"
        return context


class ResourcesView(TemplateView):
    template_name = "content/resources.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "resources"
        return context


class DashboardView(TemplateView):
    template_name = "content/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        Return dashboard queries within the context
        """
        # Genre Data
        genre_data = list(
            Genre.objects.order_by("name").values(
                "name",
                artist_count=Count("recording_artists", distinct=True),
                song_count=Count("recording_artists__songs", distinct=True),
                album_count=Count("recording_artists__albums", distinct=True),
            )
        )
        name_map = dict(Genre.GENRE_CHOICES)
        for genre in genre_data:
            genre["name"] = name_map[genre["name"]]
        context["genre_data"] = json.dumps(genre_data)

        # Artist Data
        artist_data = list(
            Artist.objects.order_by("name").values(
                "name",
                song_count=Count("songs"),
                average_length=Avg("songs__time_length"),
            )
        )
        for artist in artist_data:
            avg_length = artist["average_length"]
            if not avg_length:
                artist["average_length"] = ""
                continue
            minutes, seconds = divmod(avg_length.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days = avg_length.days
            string = ""
            if days:
                string = f"{string}{days}d "
            if hours:
                string = f"{string}{hours}h "
            if minutes:
                string = f"{string}{minutes}m "
            if seconds:
                string = f"{string}{seconds}s"
            artist["average_length"] = string
        context["artist_data"] = artist_data

        now = timezone.now()
        song_data = list(
            SongPlayLog.objects.filter(date_played__month=now.month)
            .values(artist_name=F("song__artist__name"))
            .annotate(plays=Count("*"))
            .order_by("-plays")[:10]
        )
        context["song_data"] = song_data
        context["song_data_json"] = json.dumps(song_data)

        context["active_tab"] = "dashboard"
        return context
