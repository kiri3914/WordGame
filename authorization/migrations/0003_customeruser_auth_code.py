# Generated by Django 5.0.6 on 2024-06-05 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0002_country_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="customeruser",
            name="auth_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
