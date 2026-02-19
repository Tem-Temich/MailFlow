from .models import Message
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail_messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("mail_messages.can_view_all_messages"):
            return Message.objects.all()

        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('mail_messages:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('mail_messages:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mail_messages/message_confirm_delete.html'
    success_url = reverse_lazy('mail_messages:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mail_messages/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("mail_messages.can_view_all_messages"):
            return Message.objects.all()

        return Message.objects.filter(owner=user)
