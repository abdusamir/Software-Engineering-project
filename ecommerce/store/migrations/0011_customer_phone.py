# Generated by Django 3.1.5 on 2021-01-10 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_customer_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='Phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
