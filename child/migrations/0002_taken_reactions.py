# Generated by Django 4.1.5 on 2023-04-29 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taken',
            name='reactions',
            field=models.CharField(default='null', max_length=1000),
            preserve_default=False,
        ),
    ]