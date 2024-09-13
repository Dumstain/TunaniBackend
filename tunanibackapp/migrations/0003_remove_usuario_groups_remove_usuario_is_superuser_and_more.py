# Generated by Django 5.0.3 on 2024-03-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunanibackapp', '0002_usuario_groups_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='contrasenia',
            field=models.CharField(max_length=45),
        ),
    ]
