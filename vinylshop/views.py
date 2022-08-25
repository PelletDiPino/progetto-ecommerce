from django.views.generic import TemplateView, CreateView
from django.shortcuts import render

def home(request):
    return render(request, template_name='home.html')