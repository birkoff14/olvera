# Generated by Django 3.1.4 on 2020-12-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Estado_SAT', models.CharField(blank=True, max_length=150)),
                ('Version', models.CharField(blank=True, max_length=150)),
                ('Tipo', models.CharField(blank=True, max_length=150)),
                ('Fecha_Emision', models.CharField(blank=True, max_length=150)),
                ('Fecha_Timbrado', models.CharField(blank=True, max_length=150)),
                ('Serie', models.CharField(blank=True, max_length=150)),
                ('Folio', models.CharField(blank=True, max_length=150)),
                ('UUID', models.CharField(blank=True, max_length=150)),
                ('RFC_Receptor', models.CharField(blank=True, max_length=150)),
                ('Nombre_Receptor', models.CharField(blank=True, max_length=150)),
                ('UsoCFDI', models.CharField(blank=True, max_length=150)),
                ('SubTotal', models.CharField(blank=True, max_length=150)),
                ('IVA_16', models.CharField(blank=True, max_length=150)),
                ('Total', models.CharField(blank=True, max_length=150)),
                ('Total_Trasladados', models.CharField(blank=True, max_length=150)),
                ('Moneda', models.CharField(blank=True, max_length=150)),
                ('Forma_De_Pago', models.CharField(blank=True, max_length=150)),
                ('Metodo_de_Pago', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]