# Generated by Django 4.0.7 on 2022-10-06 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photoproject', '0014_alter_projectreceipts_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='photoproject.category'),
        ),
    ]
