# Generated by Django 2.2 on 2019-05-03 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SadiCarnot10', '0005_auto_20190502_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='condomino',
            name='cargos',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='condomino',
            name='saldo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]