from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomerUser

@receiver(post_save, sender=CustomerUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            image="default.jpg",
            bio="This is a bio"
        )

    