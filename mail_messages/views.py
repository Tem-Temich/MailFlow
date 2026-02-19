from .models import Message
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import MessageForm
# Create your views here.
class MessageListView(ListView):
    model = Message
    template_name = 'mail_messages/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('mail_messages:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('mail_messages:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mail_messages/message_confirm_delete.html'
    success_url = reverse_lazy('mail_messages:message_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mail_messages/message_detail.html'
    context_object_name = 'message'
