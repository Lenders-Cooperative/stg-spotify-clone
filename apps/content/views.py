import datetime
import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum, QuerySet  # noqa
from django.views.generic import TemplateView

from music.models import SongPlayLog

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

    def _with_json(self, data: QuerySet):
        data = list(data)
        return dict(raw=data, json=json.dumps(data))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        Return dashboard queries within the context
        """
        month_start = datetime.datetime.now().replace(day=1).date()
        genres_breakdown = Genre.objects.all().annotate(songs_count=Count("songs", distinct=True),
                                                        artist_count=Count("songs__artist", distinct=True),
                                                        albums_count=Count("songs__album", distinct=True)
                                                        ).values("name", "songs_count", "artist_count",
                                                                 "albums_count").order_by("-songs_count",
                                                                                          "-artist_count",
                                                                                          "-albums_count")
        songs_breakdown = Artist.objects.all().annotate(songs_count=Count("songs"),
                                                        avg_length=Avg("songs__time_length")
                                                        ).values('name', 'songs_count', 'avg_length').order_by(
            '-songs_count', '-avg_length')
        top10 = Artist.objects.filter(songs__play_logs__date_played__gte=month_start).annotate(
            plays=Count("songs__play_logs")).values('name', 'plays').order_by('-plays')[:10]
        for x in songs_breakdown:
            # get hh:mm:ss tops
            x["avg_length"] = str(x["avg_length"] or datetime.timedelta(seconds=0))[:8]

        return dict(active_tab="dashboard",
                    genres_breakdown=self._with_json(genres_breakdown),
                    songs_breakdown=self._with_json(songs_breakdown),
                    top10=self._with_json(top10))
