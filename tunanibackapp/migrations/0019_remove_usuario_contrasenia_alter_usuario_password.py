# Generated by Django 5.0.3 on 2024-05-08 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunanibackapp', '0018_alter_usuario_datos_alter_usuario_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='contrasenia',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
