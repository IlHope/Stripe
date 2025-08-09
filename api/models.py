from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('RUB', 'Russian Ruble'),
        ('USD', 'US Dollar'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='RUB')

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveSmallIntegerField(default=0)
    stripe_promotion_code_id = models.CharField(max_length=100, help_text="Stripe Promotion Code ID")

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Tax(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.PositiveSmallIntegerField(default=0)
    stripe_tax_rate_id = models.CharField(max_length=100, help_text="Stripe Tax Rate ID")

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)
