# Generated by Django 5.0.3 on 2024-05-05 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunanibackapp', '0009_remove_producto_imagen_alter_fotos_producto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotoCooperativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.ImageField(blank=True, null=True, upload_to='imagenes_cooperativas/')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='tunanibackapp.cooperativa')),
            ],
        ),
    ]