# Generated by Django 4.1.1 on 2022-09-24 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photoproject', '0010_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='business',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='company',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='persons',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photoproject.project'),
        ),
    ]
