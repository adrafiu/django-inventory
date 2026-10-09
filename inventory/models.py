from django.conf import settings
from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("electronics", "Electronics"),
        ("clothing", "Clothing"),
        ("food", "Food"),
        ("books", "Books"),
        ("others", "Others"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="others",
    )

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(default=0)

    low_stock_threshold = models.PositiveIntegerField(default=5)

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
