from audioop import avg
from collections import Counter
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
from product.models import Category, Order, Product, VendorReview


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


class AccountDetails(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/account_info.html'

    def get_object(self):
        return self.request.user


class AccountVendorDetails(GroupRequiredMixin, DetailView):
    raise_exception = True
    group_required = ["vendors"]
    model = User
    template_name = 'account/vendor_stats_details.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        orders = Order.objects.all()

        orders_prices = []
        titles_list = []
        for order in orders:
            orders_prices.append(order.product.price)
            titles_list.append(order.product.category.title)
        
        context['avg_spent'] = round(sum(orders_prices) / len(orders_prices),2)
        context['title_list'] = titles_list

        title_count = Counter(titles_list)

        most_purchased_categories = title_count.most_common(3)

        products_titles = []
        for elem in most_purchased_categories:
            products_titles.append(elem[0])

        context['most_purchased_categories'] = products_titles

        num_reviews = 0
        total_score = 0
        
        total_vendor_reviews = VendorReview.objects.filter(vendor_id=self.get_object().id)
        context['total_vendor_reviews'] = len(total_vendor_reviews)

        for review in VendorReview.objects.filter(vendor_id=self.get_object().id):
            num_reviews += 1
            total_score += review.stars
        try:
            context['average_rating'] = int(total_score/num_reviews)
        except:
            context['average_rating'] = 0


        return context 