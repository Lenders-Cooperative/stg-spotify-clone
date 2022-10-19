import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum  # noqa
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
        context["genre_charts"] = [
            {
                "id": "songs_per_genre",
                "labels": [1, 2],
                "label": "# Songs per Genre",
                "data": [1, 2]
            },
            {
                "id": "artists_per_genre",
                "labels": [1, 2],
                "label": "# Artists per Genre",
                "data": [1, 2]
            },
            {
                "id": "albums_per_genre",
                "labels": [1, 2],
                "label": "# Albums per Genre",
                "data": [1, 2]
            }
        ]
        songs_agg_data = Song.objects.all().select_related('artist__name').values('artist', 'artist__name')

        artists = Artist.objects.order_by("name").values(
            "name",
            no_of_songs=Count("songs"),
            avg_song_len=Avg("songs__time_length"),
        )
        for artist in artists:
            duration = artist['avg_song_len']
            if not duration:
                continue
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            artist['avg_song_len'] = f"{hours}:{minutes}:{seconds}"
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
        context["top_ten_artists"] = [
            {
                "id": "top_ten_artists",
                "labels": [1, 2],
                "label": "Top 10 Artists by monthly listners",
                "data": [1, 2]
            }
        ]
        # print(context)
        return context
