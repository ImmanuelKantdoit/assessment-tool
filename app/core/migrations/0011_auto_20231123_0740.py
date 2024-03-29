# Generated by Django 3.2.23 on 2023-11-23 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_role_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='role',
            name='role',
            field=models.CharField(choices=[('examinee', 'Examinee'), ('examiner', 'Examiner'), ('admin', 'Admin'), ('super_admin', 'Super Admin')], default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.role'),
        ),
    ]
