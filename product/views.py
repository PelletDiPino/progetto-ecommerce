from django.utils import timezone
from django.contrib import messages
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from braces.views import GroupRequiredMixin
from .models import Category, Product, ProductReview, VendorReview, Order
from .forms import ProductForm, ProductReviewForm, VendorReviewForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

# Create your views here.

class CreateProduct(SuccessMessageMixin, GroupRequiredMixin, CreateView):
    raise_exception = True
    group_required = ["vendors"]
    form_class = ProductForm
    model = Product
    template_name = 'product/create.html'
    success_message = 'Prodotto aggiunto!'
    success_url = reverse_lazy('account:my_sales')

    def form_valid(self, form):
        form.instance.vendor_id = self.request.user.id
        return super().form_valid(form)

class ProductDelete(GroupRequiredMixin,SuccessMessageMixin, DeleteView):
    raise_exception = True
    group_required = ["vendors"]
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('account:my_sales')
    success_message = "Prodotto eliminato!"


class ProductUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    raise_exception = True
    group_required = ["vendors"]
    form_class = ProductForm
    model = Product
    template_name = 'product/product_update.html'
    success_url = reverse_lazy('account:my_sales')
    success_message = "Prodotto aggiornato correttamente!"

class ProductsListView(ListView):
    model = Product
    template_name = 'product/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'product/categories.html'


def category_filter_view(request,slug):
    category = Category.objects.get(slug=slug).slug
    products = Product.objects.filter(category__slug=category)
    ctx = {
        'category':category,
        'products':products
    }
    return render(request, 'product/category_filter.html', ctx)

class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar_items = Product.objects.filter(category_id=self.get_object().category_id).exclude(id=self.get_object().id)
        context['similar_items'] = similar_items
        context['already_reviewed'] = False
        context['my_review'] = None
        try:
            if self.request.user.is_authenticated:
                product = self.get_object().id
                user_id = User.objects.get(username=self.request.user).id
                review = ProductReview.objects.get(product_id=product, writer_id=user_id)

                if review:
                    context['my_review'] = review
                    context['already_reviewed'] = True
        except:
            pass

        return context



class VendorDetails(DetailView):
    model = User
    template_name = 'product/vendor_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['self_review'] = False
        context['already_reviewed'] = False
        context['my_review'] = None
        num_reviews = 0
        total_score = 0
        
        total_vendor_reviews = VendorReview.objects.filter(vendor_id=self.get_object().id)
        context['total_vendor_reviews'] = len(total_vendor_reviews)

        for review in VendorReview.objects.filter(vendor_id=self.get_object().id):
            num_reviews += 1
            total_score += review.stars
        try:
            context['average_rating'] = round(float(total_score/num_reviews),2)
        except:
            context['average_rating'] = 0

        try:
            if self.request.user.is_authenticated:
                vendor_id = self.get_object().id
                user_id = User.objects.get(username=self.request.user).id
                review = VendorReview.objects.get(writer_id=user_id, vendor_id=vendor_id)

                if review:
                    context['my_review'] = review
                    context['already_reviewed'] = True
        except:
            pass

        try:
            if self.request.user.is_authenticated:
                vendor_id = self.get_object().id
                writer_id = User.objects.get(username=self.request.user).id
                if vendor_id == writer_id:
                    context['self_review'] = True
        except:
            pass

        return context 

def productReview(request, slug):
    template = 'product/product_review.html'
    ctx = {
        'form': ProductReviewForm(),
        "message": '',
        "vendor": None,
        "product": slug
    }

    if request.method == "POST":
        form = ProductReviewForm(request.POST)

        if form.is_valid():
            review = ProductReview()
            review.stars = form.cleaned_data.get('review_value')
            review.text = form.cleaned_data.get('review_text')
            review.product = Product.objects.get(slug=slug)
            review.writer = User.objects.get(username=request.user.username)
            
            review.save()
            messages.success(request,"Grazie per la recensione!")
            return redirect("product:product_details", slug)

    return render(request, template_name=template, context=ctx)


def vendorReview(request, pk):
    template = 'product/product_review.html'
    ctx = {
        'form': VendorReviewForm(),
        'vendor': pk
    }

    if request.method == "POST":
        form = VendorReviewForm(request.POST)

        if form.is_valid():
            review = VendorReview()
            review.stars = form.cleaned_data.get('review_value')
            review.writer = User.objects.get(username=request.user.username)
            review.vendor = User.objects.get(id=pk)

            review.save()
            messages.success(request,"Grazie per la recensione!")
            return redirect("product:vendor_details", pk)

    return render(request, template_name=template, context=ctx)



class BuyProduct(LoginRequiredMixin, DetailView):
    success_url = reverse_lazy('product:product_details')
    template_name = 'product/product_buy.html'
    model = Product


def add_order(request,slug):
    order = Order(
            customer = User.objects.get(id=request.user.id),
            product = Product.objects.get(slug=slug),
            created_at = timezone.now(),
        )
    order.save()
    messages.success(request,"Acquisto effettuato correttamente!")
    return redirect('product:product_details', slug)


def search(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(Q(title__icontains=query) | Q(category__title__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'product/search.html', {'products':products, 'query':query})


def search_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price == '' or max_price == '':
        return redirect('product:list_products')
        
    if min_price > max_price:
         return redirect('product:list_products')

    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)

    ctx = {
        'min_price':min_price,
        'max_price':max_price,
        'products':products
    }

    return render(request, 'product/price_search.html', ctx)