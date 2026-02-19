from .models import Client
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ClientForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'client_list'

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("clients.can_view_all_clients"):
            return Client.objects.all()

        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_create.html'
    success_url = reverse_lazy('clients:clients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_delete.html'
    success_url = reverse_lazy('clients:clients_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("clients.can_view_all_clients"):
            return Client.objects.all()

        return Client.objects.filter(owner=user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_update.html'
    success_url = reverse_lazy('clients:clients_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)
