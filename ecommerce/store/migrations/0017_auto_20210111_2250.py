# Generated by Django 3.1.5 on 2021-01-11 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210111_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='products',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]