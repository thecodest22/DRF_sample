from django.db import models
from django.db.models import Index
from django.db.models.functions import Upper


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            Index(
                Upper('name'),
                name='product_name_upper_idx',
            ),
        ]

    def __str__(self):
        return self.name
