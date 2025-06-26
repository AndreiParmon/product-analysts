from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discounted_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    rating = models.FloatField()
    review_count = models.IntegerField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

