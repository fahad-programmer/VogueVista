# Generated by Django 5.0.6 on 2024-05-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_alter_companyprofile_about_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(max_length=50),
        ),
    ]