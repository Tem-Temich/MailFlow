
from .models import Client
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ClientForm
# Create your views here.

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'client_list'
    def get_queryset(self):
        return Client.objects.all()

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_create.html'
    success_url = reverse_lazy('clients:clients_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_delete.html'
    success_url = reverse_lazy('clients:clients_list')

class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_update.html'
    success_url = reverse_lazy('clients:clients_list')