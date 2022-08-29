from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, View
from braces.views import GroupRequiredMixin
from .models import Product, ProductReview, VendorReview
from .forms import ProductForm, ProductReviewForm, VendorReviewForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User


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
    template_name = 'product/product_list.html'


class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['is_reviewed'] = False

        try:
            if self.request.user.is_authenticated:
                productId = self.get_object().id
                userId = User.objects.get(username=self.request.user).id
                review = ProductReview.objects.get(product_id=productId, user_id=userId)

                if review:
                    context['is_reviewed'] = True
        except:
            pass

        return context

class VendorDetails(DetailView):
    model = User
    template_name = 'product/vendor_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_reviewed'] = False

        num_reviews = 0
        total_score = 0

        for score in VendorReview.objects.filter(vendor_id=self.get_object().id):
            num_reviews += 1
            total_score += score.stars
        try:
            context['average_rating'] = int(total_score/num_reviews)
        except:
            context['average_rating'] = 0

        try:
            if self.request.user.is_authenticated:
                vendorId = self.get_object().id
                userId = User.objects.get(username=self.request.user).id
                review = VendorReview.objects.filter(vendor_id=vendorId, user_id=userId)

                if len(review) > 0:
                    context['isReviewed'] = True
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
            score = ProductReview()
            score.stars = form.cleaned_data.get('review_value')
            score.text = form.cleaned_data.get('review_text')
            score.product = Product.objects.get(slug=slug)
            score.writer = User.objects.get(username=request.user.username)
            
            score.save()

            return redirect("product:product_details", slug)

    return render(request, template_name=template, context=ctx)


def vendorReview(request, pk):
    template = 'product/product_review.html'
    ctx = {
        'form': VendorReviewForm(),
        "message": '',
        "vendor": pk
    }

    if request.method == "POST":
        form = VendorReviewForm(request.POST)

        if form.is_valid():
            score = VendorReview()
            score.stars = form.cleaned_data.get('review_value')
            score.writer = User.objects.get(username=request.user.username)
            score.vendor = User.objects.get(id=pk)

            score.save()

            return redirect("product:vendor_details", pk)

    return render(request, template_name=template, context=ctx)
