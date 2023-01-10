import datetime
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
        genres = Genre.objects.select_related("songs").prefetch_related(
            "songs__album", "songs__genre"
        ).annotate(
            songs_count=Count("songs", distinct=True),
            artists=Count("songs__artist", distinct=True),
            albums=Count("songs__album", distinct=True)
        ).values("name", "songs_count", "artists", "albums")
        genres = json.dumps(list(genres))
        context["genres"] = genres
        context["active_tab"] = "dashboard"
        return context


class ArtistsView(TemplateView):
    template_name = "content/artists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """  
        Return dashboard queries within the context 
        """
        artists = Artist.objects.select_related("songs").annotate(
            songs_count=Count("songs"),
            average_length=Avg("songs__time_length", distinct=True)
        ).values("name", "songs_count", "average_length").order_by("name")
        context["artists"] = artists
        context["active_tab"] = "artists"
        return context

class TopArtistsView(TemplateView):
    template_name = "content/top_artists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """  
        Return dashboard queries within the context 
        """
        current_month = datetime.datetime.now().month
        artists = Artist.objects.select_related("songs").prefetch_related(
            "songs__play_logs"
        ).annotate(
            play_counts=Count(
                "songs__play_logs",
                filter=Q(songs__play_logs__date_played__month__gte=current_month)
            )
        ).values("name", "play_counts").order_by("-play_counts")[:10]
        context["artists"] = artists
        context["active_tab"] = "top_artists"
        return context
