# Generated by Django 5.1.5 on 2025-06-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_job_job_type_job_company_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.IntegerField(),
        ),
    ]
