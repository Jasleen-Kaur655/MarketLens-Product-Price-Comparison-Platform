from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flipkart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    myntra_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


