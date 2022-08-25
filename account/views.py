from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy