from django import forms
from .models import Product, ProductReview, VendorReview


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'category']

class VendorReviewForm(forms.Form):
    CHOICE_LIST = [(i,i) for i in range(1,6)]
    review_value = forms.ChoiceField(
        label="Punteggio ",
        required=True,
        choices=CHOICE_LIST
    )

class ProductReviewForm(forms.Form):
    CHOICE_LIST = [(i,i) for i in range(1,6)]
    review_value = forms.ChoiceField(
        label="Punteggio ",
        required=True,
        choices=CHOICE_LIST
    )
    review_text = forms.CharField()