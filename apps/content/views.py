from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum  # noqa
from django.views.generic import TemplateView

User = get_user_model()
Profile = apps.get_model("users", "Profile")
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
        return context
