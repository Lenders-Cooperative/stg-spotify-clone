from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum  # noqa
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views.generic import TemplateView

User = get_user_model()
Profile = apps.get_model("users", "Profile")
RecordLabel = apps.get_model("music", "RecordLabel")
Playlist = apps.get_model("music", "Playlist")
Album = apps.get_model("music", "Album")
Artist = apps.get_model("music", "Artist")
Song = apps.get_model("music", "Song")
SongPlayLog = apps.get_model("music", "SongPlayLog")
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

        # Song and PlayLog count per Genre
        song_count = Song.objects.values("genre").annotate(count=Count("genre"))
        play_count = SongPlayLog.objects.values("song__genre").annotate(count=Count("song__genre"))
        artists = SongPlayLog.objects.values("song__artist", "song__artist__name").annotate(count=Count("song__artist"))
        context["genres_summary"] = {
            "labels": Song.Genre.labels,
            "songs": list(song_count.values_list("count", flat=True)),
            "plays": list(play_count.values_list("count", flat=True)),
        }

        # Top artists by month
        months = []
        start = now()
        try:
            active = parse_date(self.request.GET.get("month")) or start
        except (ValueError, TypeError):
            active = start
        for i in range(-5, 1):
            date = start + relativedelta(months=i)
            is_active = (date.month, date.year) == (active.month, active.year)
            months.append((is_active, date))
        context["months"] = months
        context["top_artists"] = artists.filter(date_played__year=active.year, date_played__month=active.month).order_by("-count")[:10]

        # Song stats
        avg_duration = Song.objects.aggregate(Avg("time_length"))["time_length__avg"]
        context["song_stats"] = {
            "duration": str(avg_duration).split(".")[0],
            "album": Album.objects.annotate(count=Count("songs")).aggregate(Avg("count"))["count__avg"],
            "artist": Artist.objects.annotate(count=Count("songs")).aggregate(Avg("count"))["count__avg"],
            "genre": song_count.aggregate(Avg("count"))["count__avg"],
        }
        return context
