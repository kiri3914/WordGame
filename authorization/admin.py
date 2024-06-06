from django.contrib import admin
from .models import CustomerUser, Country, Profile

admin.site.register(CustomerUser)
admin.site.register(Country)
admin.site.register(Profile)