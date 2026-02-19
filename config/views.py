from django.views.generic import TemplateView
from django.utils import timezone
from clients.models import Client
from mailings.models import Mailing


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        ).count()
        context["total_clients"] = Client.objects.count()

        return context