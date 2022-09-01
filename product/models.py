from django.contrib.auth.models import User
from django.db import models

from django_extensions.db.fields import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from='title')

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from='title')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def get_reviews_num(self):
        reviews = ProductReview.objects.filter(product=self)
        return len(reviews)

    def get_reviews(self):
        reviews = ProductReview.objects.filter(product=self)
        review_details = []

        for review in reviews:
            review_details.append((review))
        
        return review_details

    def get_average_score(self):
        total_score = 0
        reviews = ProductReview.objects.filter(product=self)
        num_reviews = len(reviews)

        if num_reviews != 0:
            for review in reviews:
                total_score += review.stars
        
            return float(total_score/num_reviews)
        
        return 0


class Review(models.Model):
    
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stars = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    class Meta:
        abstract = True

class ProductReview(Review):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VendorReview(Review):
    vendor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="vendor")
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)