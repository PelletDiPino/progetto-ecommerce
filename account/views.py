from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/user_creation.html'
    success_url = reverse_lazy("login")