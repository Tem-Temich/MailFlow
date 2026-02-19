from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView, View, TemplateView
from .forms import MailingForm
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Mailing, Attempt


# Create your views here.
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        user = self.request.user

        if (
                user.has_perm("mailings.can_view_all_mailings")
                or user.has_perm("mailings.can_disable_mailing")
        ):
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["can_disable"] = self.request.user.has_perm(
            "mailings.can_disable_mailing"
        )

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        user = self.request.user

        if (
                user.has_perm("mailings.can_view_all_mailings")
                or user.has_perm("mailings.can_disable_mailing")
        ):
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object

        context["total_recipients"] = mailing.recipients.count()
        context["success_attempts"] = mailing.attempt_set.filter(status="success").count()
        context["failed_attempts"] = mailing.attempt_set.filter(status="failed").count()

        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_delete.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingSendView(LoginRequiredMixin, View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        now = timezone.now()

        # Проверка времени
        if not (mailing.start_time <= now <= mailing.end_time):
            messages.error(request, "Рассылка сейчас недоступна для отправки.")
            return redirect('mailings:mailing_detail', pk=pk)

        recipients = mailing.recipients.all()

        if not recipients.exists():
            messages.error(request, "Нет получателей для этой рассылки.")
            return redirect('mailings:mailing_detail', pk=pk)

        success_count = 0
        if not mailing.is_active:
            messages.error(request, "Рассылка отключена менеджером.")
            return redirect("mailings:mailing_list")

        if mailing.status != "started":
            messages.error(request, "Рассылка сейчас недоступна для отправки.")
            return redirect("mailings:mailing_list")

        for client in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                Attempt.objects.create(
                    mailing=mailing,
                    status='success',
                    server_response='OK'
                )

                success_count += 1

            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    server_response=str(e)
                )

        messages.success(request, f"Отправлено писем: {success_count}")

        return redirect('mailings:mailing_detail', pk=pk)


@method_decorator(cache_page(60), name="dispatch")
class MailingReportView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)

        report_data = []

        for mailing in mailings:
            attempts = Attempt.objects.filter(mailing=mailing)

            total = attempts.count()
            success = attempts.filter(status="succeeded").count()
            failed = attempts.filter(status="failed").count()

            report_data.append({
                "mailing": mailing,
                "total": total,
                "success": success,
                "failed": failed,
            })

        context["report_data"] = report_data
        return context


class MailingDisableView(LoginRequiredMixin, View):

    def post(self, request, pk):
        if not request.user.has_perm("mailings.can_disable_mailing"):
            messages.error(request, "Недостаточно прав.")
            return redirect("mailings:mailing_list")

        mailing = get_object_or_404(Mailing, pk=pk)

        mailing.is_active = False
        mailing.save()

        messages.success(request, "Рассылка отключена.")
        return redirect("mailings:mailing_list")
