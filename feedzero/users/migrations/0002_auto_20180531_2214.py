# Generated by Django 2.0.5 on 2018-05-31 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="feedzerouser",
            name="watching",
            field=models.ManyToManyField(
                blank=True, related_name="watched_by", to="feeds.Feed"
            ),
        )
    ]
