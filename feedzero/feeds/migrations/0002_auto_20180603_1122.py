# Generated by Django 2.0.6 on 2018-06-03 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("feeds", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="enclosure",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enclosures",
                to="feeds.Entry",
            ),
        )
    ]
