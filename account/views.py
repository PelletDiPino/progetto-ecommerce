from braces.views import GroupRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from account.forms import UserCreationCustomForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from product.models import Order, Product


class UserCreateView(CreateView):
    form_class = UserCreationCustomForm
    template_name = 'account/user_creation.html'
    success_url = reverse_lazy("homepage")

    def form_valid(self,form):
        valid = super().form_valid(form)
        user = form.save(commit=False)
        user.save()

        if form.cleaned_data['is_vendor']:
            user_group = Group.objects.get(name="vendors")
            user.groups.add(user_group)
        
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password1'],
        )

        messages.info(self.request, "Registration complete!")
        login(self.request, user)

        return valid


class UserLogin(LoginView):
    template_name = 'account/login.html'
    next_page = reverse_lazy('homepage')

class UserLogout(LogoutView):
    template_name = 'account/logout.html'
    next_page = reverse_lazy('homepage')


class MySales(GroupRequiredMixin, ListView):

    raise_exception = True
    group_required = ["vendors"]
    model = Product
    template_name = 'account/my_sales.html'

    def get_queryset(self):
        return Product.objects.all().filter(vendor=self.request.user)

  
class MySalesDetails(GroupRequiredMixin, DetailView):
    raise_exception = True
    group_required = ["vendors"]
    model = Product
    template_name = 'account/sale_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        prod_id = self.get_object().id
        orders = Order.objects.filter(product_id=prod_id)

        context['sold_products'] = len(orders)
        context['total_income'] = context['sold_products']*self.get_object().price

        return context