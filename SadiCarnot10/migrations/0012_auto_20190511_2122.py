# Generated by Django 2.2 on 2019-05-12 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SadiCarnot10', '0011_auto_20190510_2131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registro',
            options={'managed': True, 'ordering': ['fecha'], 'verbose_name_plural': 'Registros'},
        ),
    ]
