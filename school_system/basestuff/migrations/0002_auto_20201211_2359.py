# Generated by Django 3.1.3 on 2020-12-11 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basestuff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendbaseuser',
            name='image',
            field=models.ImageField(blank=True, default='/static/default.jpg', upload_to='profiles/<django.db.models.fields.CharField>/'),
        ),
    ]