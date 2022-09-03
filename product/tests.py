from django.test import TestCase
from .models import Product
# Create your tests here.
class FunctionTest(TestCase):
    def test_get_average_score_with_no_reviews(self):
        product = Product(
            title = "test",
            description= "product with no reviews",
            price = 99.99
        )
        self.assertEqual(product.get_average_score(), 0)