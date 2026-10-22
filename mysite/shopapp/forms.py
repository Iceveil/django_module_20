from django import forms
from django.contrib.auth.models import Group

from .models import Product, Order

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=80)
#     description = forms.CharField(label='Product Description', widget=forms.Textarea(attrs={
#         'rows': '5',
#         'cols': '30'
#     }),
#                                   validators=[validators.RegexValidator(
#                                       regex=r'gsm',
#                                       message='Поле должно содержать слово gsm '
#                                   )])
#     price = forms.DecimalField(min_value=1, max_value=100000000000, decimal_places=2)

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = 'name', 'price', 'description', 'discount'


class OrderForm(forms.ModelForm):
    # product = forms.ModelMultipleChoiceField(
    #     queryset=Product.objects.all(),
    #     label="Выберете из списка:",
    # )
    class Meta:
        model = Order
        fields = 'delivery_address', 'user',  'promocode', 'product'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    images = forms.ImageField(
        widget=forms.FileInput()
    )


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()