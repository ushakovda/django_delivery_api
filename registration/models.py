import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ParcelType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(100)])
    content_value_usd = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(10000)])
    delivery_cost_rub = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    parcel_type = models.ForeignKey(ParcelType, on_delete=models.PROTECT)
    session_id = models.UUIDField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return f"{self.name} ({self.parcel_type})"
