from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "quantity",
        "owner",
        "created_at",
    )

    list_filter = (
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
