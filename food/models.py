from django.db import models

from django.urls import reverse
from django.conf import settings


# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=50, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Item(models.Model):
#     def __str__(self):
#         return self.item_name
#
#
#     user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     item_name = models.CharField(max_length=200)
#     item_description = models.CharField(max_length=200)
#     item_price = models.DecimalField(max_digits=5, decimal_places=2)
#     item_image = models.CharField(max_length=500,
#                                   default="https://www.thefuzzyduck.co.uk/wp-content/uploads/2024/05/image-coming"
#                                           "-soon-placeholder-01-660x660.png")
#
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='items'
#     )
#     ingredients = models.TextField(
#         blank=True,
#         help_text="Comma-separate the ingredients"
#     )
#
#     def get_absolute_url(self):
#         return reverse('food:detail', kwargs={'pk': self.pk})
#
#
# # new
# class CustomCombo(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='custom_combos'
#     )
#     name = models.CharField(max_length=100)
#     items = models.ManyToManyField('Item')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.name} by {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self): return self.name


class Item(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items_created'
    )
    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)
    item_image = models.CharField(
        max_length=500,
        default="https://…placeholder.png"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='items'
    )
    ingredients = models.TextField(
        blank=True,
        help_text="Comma-separate the ingredients"
    )

    def __str__(self): return self.item_name

    def get_absolute_url(self):
        return reverse('food:detail', kwargs={'pk': self.pk})


class CustomCombo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_combos'
    )
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"
