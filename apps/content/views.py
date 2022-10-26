from datetime import date
from optparse import Values
from tokenize import group
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Func, Q, Sum  # noqa
from django.views.generic import TemplateView
from django.db.models.functions import TruncMonth,Substr,Cast
from datetime import datetime

User = get_user_model()
Profile = apps.get_model("users", "Profile")
Genre = apps.get_model("music", "Genre")
RecordLabel = apps.get_model("music", "RecordLabel")
Playlist = apps.get_model("music", "Playlist")
Album = apps.get_model("music", "Album")
Artist = apps.get_model("music", "Artist")
SongPlayLog = apps.get_model("music", "SongPlayLog")
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
        context["songs_artiest_info"] = Artist.objects.values('name').annotate(
            songs_no=Count('songs__pk'),song_played_no=Count('songs__play_logs')).order_by('name')
        
        context["albums_artiest_info"] = Artist.objects.values('name').annotate(
            albums_no=Count('albums__pk')).order_by('name')
        
        context["avg_of_songs"] = Artist.objects.values('name').annotate(
            avg_songs=Avg('songs__time_length'))
        
        
        context["months"] = SongPlayLog.objects.annotate(months=TruncMonth('date_played')).values_list('months').distinct().order_by('-months')
        # print(context["months"])
        month = self.request.GET.get('date_month')
        
        if month:            
            context["top_artiests"] = Artist.objects.annotate(
                months=TruncMonth('songs__play_logs__date_played')).filter(months=month).values(
                'name','months').annotate(played_songs_no=Count('songs__play_logs')).values('name','months').order_by('-played_songs_no')[:10]
        
        context["top_artiests"] = Artist.objects.annotate(
            months=TruncMonth('songs__play_logs__date_played')).values(
            'name','months').annotate(played_songs_no=Count('songs__play_logs')).values('name','months').order_by('-months')[0]
                
    
        context["active_tab"] = "dashboard"
        return context
    
    
     