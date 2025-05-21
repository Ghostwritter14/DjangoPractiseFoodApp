from django.db import models
from django.contrib.auth.models import User

from food.models import Category


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pics')
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    favorite = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='favorited_by_users',
        help_text="Your single favorite food category"
    )

    def __str__(self):
        return self.user.username