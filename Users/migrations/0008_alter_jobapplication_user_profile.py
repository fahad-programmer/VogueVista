# Generated by Django 5.0.6 on 2024-05-23 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_alter_jobapplication_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='Users.userprofile'),
        ),
    ]