from django.db import models
from django.conf import settings
from food.models import Item


# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('on_the_way', 'On the way'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='pending')

    @property
    def total_price(self):
        return sum(oi.subtotal for oi in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    item = models.ForeignKey(Item,
                             on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantity * self.item.item_price
