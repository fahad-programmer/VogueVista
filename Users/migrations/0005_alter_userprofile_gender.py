# Generated by Django 5.0.6 on 2024-05-16 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
    ]
