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

        context["active_tab"] = "dashboard"
        genres = Genre.objects.all().select_related("songs", "songs__artist", "songs__album").values("name", no_of_songs=Count('songs', distinct=True), no_of_artists=Count('songs__artist', distinct=True), no_of_albums=Count('songs__album', distinct=True))
        genre_chart_labels = json.dumps([genre["name"] for genre in genres])
        context["genre_charts"] = [
            {
                "id": "songs_per_genre",
                "labels": genre_chart_labels ,
                "label": "# Songs per Genre",
                "data": [genre["no_of_songs"] for genre in genres]
            },
            {
                "id": "artists_per_genre",
                "labels":genre_chart_labels,
                "label": "# Artists per Genre",
                "data": [genre["no_of_artists"] for genre in genres]
            },
            {
                "id": "albums_per_genre",
                "labels": genre_chart_labels,
                "label": "# Albums per Genre",
                "data": [genre["no_of_albums"] for genre in genres]
            }
        ]

        artists = Artist.objects.all().select_related("songs").order_by("name").values(
            "name",
            no_of_songs=Count("songs"),
            avg_song_len=Avg("songs__time_length"),
        )
        for artist in artists:
            duration = artist['avg_song_len']
            if not duration:
                continue
            # hours, remainder = divmod(duration.seconds, 3600)
            # minutes, seconds = divmod(remainder, 60)
            # doing comparison in seconds in the chart
            seconds = duration.seconds
            artist['avg_song_len'] = f"{seconds}"
        context["songs_chart"] = [
            {
                "id": "songs_per_artist",
                "labels": json.dumps([artist["name"] for artist in artists]),
                "label": "# Songs per Artist",
                "data": [artist["no_of_songs"] for artist in artists]
            },
            {
                "id": "avg_song_duration_per_artist",
                "labels": json.dumps([artist["name"] for artist in artists]),
                "label": "Avg. Song duration per artist",
                "data": json.dumps([artist["avg_song_len"] for artist in artists])
            }
        ]

        # artists = Artist.objects.all().prefetch_related('songs', 'songs__play_logs').annotate().order_by('songs__play_logs')

        play_logs = SongPlayLog.objects.select_related('song').filter(date_played__month=timezone.now().month).values(artist_name=F("song__artist__name")).annotate(no_of_plays=Count("*")).order_by("-no_of_plays")[:10]

        context["top_ten_artists"] = [
            {
                "id": "top_ten_artists",
                "labels": json.dumps([play_log["artist_name"] for play_log in play_logs]),
                "label": "Top 10 Artists by monthly listners",
                "data": [play_log["no_of_plays"] for play_log in play_logs]
            }
        ]
        # print(context)
        return context
