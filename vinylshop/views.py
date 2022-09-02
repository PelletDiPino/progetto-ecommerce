from django.db.models import Case, When
from unicodedata import category
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render
from collections import Counter
from product.models import Product, Order

def home(request):
    
    orders = Order.objects.all()
    orders_list = []

    for order in orders:
        orders_list.append(order.product.id)

    count = Counter(orders_list)

    most_commons = count.most_common(5)

    products_id = []
    for prod_id in most_commons:
        products_id.append(prod_id[0])
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(products_id)])
    top_sellers = Product.objects.filter(id__in=products_id).order_by(preserved)
    
    ctx = {
        'top_sellers':top_sellers
    }
    return render(request, template_name='home.html', context=ctx)

