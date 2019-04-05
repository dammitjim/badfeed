# Generated by Django 2.2 on 2019-04-05 14:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("feeds", "0006_auto_20190107_0011")]

    operations = [
        migrations.CreateModel(
            name="EnrichedContent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("summary", models.TextField()),
                (
                    "images",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=500),
                        blank=True,
                        size=None,
                    ),
                ),
                (
                    "movies",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=500),
                        blank=True,
                        size=None,
                    ),
                ),
                (
                    "entry",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enriched",
                        to="feeds.Entry",
                    ),
                ),
            ],
        )
    ]
