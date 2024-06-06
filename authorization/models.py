from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    auth_code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username