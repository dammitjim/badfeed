# Generated by Django 2.1.5 on 2019-01-08 22:57

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0002_auto_20180531_2214")]

    operations = [
        migrations.CreateModel(
            name="ThirdPartyTokens",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=255)),
                ("provider", models.CharField(choices=[("pocket", "Pocket")], max_length=50)),
                ("metadata", django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="third_party_tokens",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(name="thirdpartytokens", unique_together={("provider", "user")}),
    ]