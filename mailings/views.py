from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView, View
from .forms import MailingForm
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from mail_messages.forms import MessageForm
from .models import Mailing,Attempt
# Create your views here.
class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailings/mailing_list.html'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object

        context["total_recipients"] = mailing.recipients.count()
        context["success_attempts"] = mailing.attempt_set.filter(status="success").count()
        context["failed_attempts"] = mailing.attempt_set.filter(status="failed").count()

        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_delete.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingSendView(View):

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

