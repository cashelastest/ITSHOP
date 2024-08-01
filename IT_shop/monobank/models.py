from django.db import models


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    currency = models.PositiveIntegerField()
    reference = models.CharField(max_length=100)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
