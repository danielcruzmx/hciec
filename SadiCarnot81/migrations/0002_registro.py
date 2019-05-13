# Generated by Django 2.2 on 2019-05-12 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Catalogos', '0004_auto_20190429_1144'),
        ('SadiCarnot81', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('debe', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Depositos')),
                ('haber', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Cargos')),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('a_favor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='sadiochouno_aux_proveedor_id', to='Catalogos.Proveedore')),
                ('condomino', models.ForeignKey(default=67, on_delete=django.db.models.deletion.PROTECT, related_name='sadiochouno_aux_condomino_id', to='SadiCarnot81.Condomino')),
                ('cuenta_contable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sadiochouno_asiento_cuenta', to='Catalogos.CuentaContable', verbose_name='Cuenta Contable')),
                ('tipo_movimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sadiochouno_aux_tipo_mov_id', to='Catalogos.TipoMovimiento')),
            ],
            options={
                'verbose_name_plural': 'Registros',
                'db_table': 'sadiochouno_registro',
                'ordering': ['fecha'],
                'managed': True,
            },
        ),
    ]