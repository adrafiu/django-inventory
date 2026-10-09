from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "name",
            "sku",
            "category",
            "description",
            "price",
            "quantity",
            "low_stock_threshold",
            "purchase_date",
            "expiry_date",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
            "purchase_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "expiry_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get("expiry_date")
        purchase_date = self.cleaned_data.get("purchase_date")

        if expiry_date and purchase_date:
            if expiry_date < purchase_date:
                raise forms.ValidationError(
                    "Expiry date cannot be before purchase date."
                )

        return expiry_date


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
    
    
