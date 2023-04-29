# Generated by Django 4.1.5 on 2023-04-29 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccine', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')])),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_by', to=settings.AUTH_USER_MODEL)),
                ('vaccines_taken', models.ManyToManyField(related_name='done', to='vaccine.vaccine')),
                ('vaccines_to_take', models.ManyToManyField(related_name='upcoming', to='vaccine.vaccine')),
            ],
        ),
    ]
