# Generated by Django 2.0.6 on 2018-06-13 16:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feeds", "0004_auto_20180613_1604"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="entrystate", unique_together={("state", "user", "entry")}
        )
    ]
