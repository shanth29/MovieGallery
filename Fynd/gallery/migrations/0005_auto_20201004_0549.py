# Generated by Django 3.1.1 on 2020-10-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_usersearchhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersearchhistory',
            name='mobile',
            field=models.IntegerField(),
        ),
    ]