# Generated by Django 2.0.5 on 2018-05-21 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=255)),
                ("link", models.CharField(blank=True, max_length=1000, null=True)),
                ("email", models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Enclosure",
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
                ("href", models.CharField(max_length=1000)),
                ("file_type", models.CharField(max_length=1000)),
                ("length", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Entry",
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
                ("slug", models.SlugField(blank=True, max_length=200)),
                ("title", models.CharField(max_length=1000)),
                ("link", models.CharField(max_length=1000)),
                ("guid", models.CharField(max_length=1000)),
                ("content", models.TextField()),
                ("summary", models.TextField(blank=True, null=True)),
                ("date_published", models.DateTimeField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="entries",
                        to="feeds.Author",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        related_name="contributed_to", to="feeds.Author"
                    ),
                ),
            ],
            options={"verbose_name_plural": "entries"},
        ),
        migrations.CreateModel(
            name="Feed",
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
                ("slug", models.SlugField(blank=True, max_length=200)),
                ("title", models.CharField(max_length=255)),
                ("link", models.CharField(max_length=1000, unique=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("date_last_scraped", models.DateTimeField(blank=True, null=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("term", models.CharField(max_length=255)),
                ("scheme", models.CharField(blank=True, max_length=255, null=True)),
                ("label", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "feed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="feeds.Feed",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="entry",
            name="feed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to="feeds.Feed",
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="tags",
            field=models.ManyToManyField(related_name="entries", to="feeds.Tag"),
        ),
        migrations.AddField(
            model_name="enclosure",
            name="entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="feeds.Entry"
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="feed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authors",
                to="feeds.Feed",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="entry", unique_together={("guid", "feed")}
        ),
    ]