# Generated by Django 2.2 on 2019-04-28 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Catalogos', '0002_cuentacontable'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodocorte',
            name='saldo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]