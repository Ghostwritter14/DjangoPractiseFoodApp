from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    def __str__(self):
        return self.item_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)
    item_image = models.CharField(max_length=500,
                                  default="https://www.thefuzzyduck.co.uk/wp-content/uploads/2024/05/image-coming"
                                          "-soon-placeholder-01-660x660.png")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )
    ingredients = models.TextField(
        blank=True,
        help_text="Comma-separate the ingredients"
    )

    def get_absolute_url(self):
        return reverse('food:detail', kwargs={'pk': self.pk})
