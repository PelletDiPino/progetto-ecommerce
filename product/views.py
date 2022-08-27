from django.views.generic.list import ListView
from django.shortcuts import render
from django.views.generic import CreateView
from braces.views import GroupRequiredMixin
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
# Create your views here.

class CreateProduct(GroupRequiredMixin, CreateView):

    raise_exception = True
    group_required = ["vendors"]
    form_class = ProductForm
    model = Product
    template_name = 'product/create.html'
    success_url = reverse_lazy('account:my_sales')

    def form_valid(self, form):
        form.instance.vendor_id = self.request.user.id
        return super().form_valid(form)


class ProductsListView(ListView):
    model = Product
    template_name = 'product_list.html'

