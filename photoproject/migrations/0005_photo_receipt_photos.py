# Generated by Django 4.1.1 on 2022-09-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoproject', '0004_receipt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo/Data%y/%m/%d/')),
            ],
        ),
        migrations.AddField(
            model_name='receipt',
            name='photos',
            field=models.ManyToManyField(to='photoproject.photo'),
        ),
    ]
