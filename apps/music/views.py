from django.views.generic import TemplateView

from .models import Song


class CatalogView(TemplateView):
    template_name = "content/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "catalog"
        context["songs"] = Song.objects.select_related("artist", "album").all().order_by("name")
        return context
