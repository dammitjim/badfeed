# Generated by Django 2.2.4 on 2019-08-26 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("feeds", "0008_auto_20190423_1803")]

    operations = [
        migrations.AddField(
            model_name="feed",
            name="logo",
            field=models.FileField(blank=True, null=True, upload_to="feeds/logo/"),
        ),
        migrations.AlterField(
            model_name="feed",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
