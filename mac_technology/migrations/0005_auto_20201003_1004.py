# Generated by Django 3.1.1 on 2020-10-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mac_technology', '0004_vacancy_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy_detail',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='vacancy_detail',
            name='work_type',
        ),
        migrations.AddField(
            model_name='vacancy_detail',
            name='contract_time',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
