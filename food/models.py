from django.db import models

# Create your models here.
class Item(models.Model):
    def __str__(self):
        return self.item_name
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)