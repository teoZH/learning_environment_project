# Generated by Django 3.1.4 on 2020-12-13 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_stuff_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
