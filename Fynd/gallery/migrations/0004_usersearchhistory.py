# Generated by Django 3.1.1 on 2020-10-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_phoneotp'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=256)),
                ('movie_name', models.TextField()),
            ],
        ),
    ]
