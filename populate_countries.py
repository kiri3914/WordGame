import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from authorization.models import Country

countries = [
    "Kazakhstan",
    "Russia",
    "USA",
    "Canada",
    "Germany",
    "France",
    "Japan",
    "China",
    "Australia",
    "Brazil"
]

for country in countries:
    Country.objects.get_or_create(name=country)

print("Countries populated!")
