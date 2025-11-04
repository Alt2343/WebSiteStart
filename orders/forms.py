from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'delivery_method', 'address', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем адрес необязательным, если самовывоз
        self.fields['address'].required = False
        self.fields['city'].required = False