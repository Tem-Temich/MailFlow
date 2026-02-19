from django.views.generic import CreateView

from .forms import UserRegisterForm
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    fields = ["email", "phone", "country", "avatar"]
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user
