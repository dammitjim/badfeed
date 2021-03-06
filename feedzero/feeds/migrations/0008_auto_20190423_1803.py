# Generated by Django 2.2 on 2019-04-23 18:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("feeds", "0007_enrichedcontent")]

    operations = [
        migrations.AlterField(
            model_name="enrichedcontent",
            name="images",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=500),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="enrichedcontent",
            name="movies",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=500),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="entrystate",
            name="state",
            field=models.CharField(
                choices=[
                    ("unread", "Unread"),
                    ("read", "Read"),
                    ("hidden", "Hidden"),
                    ("saved", "Saved"),
                    ("deleted", "Deleted"),
                    ("pinned", "Pinned"),
                ],
                max_length=50,
            ),
        ),
    ]
