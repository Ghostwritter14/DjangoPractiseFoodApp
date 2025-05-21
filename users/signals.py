from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from food.models import Category
from .models import Profile


@receiver(post_save, sender=User)
def build_profile_and_choices(sender, instance, created, **kwargs):
    if created:
        # 1) Create Profile
        Profile.objects.create(user=instance)
        # 2) Create a special Category for this user
        slug = f"{instance.username}-choice"
        Category.objects.get_or_create(
            slug=slug,
            defaults={'name': f"{instance.username}'s Choices"}
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
