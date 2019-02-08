import csv
import itertools
import os
import random

from django.core.management import BaseCommand
from model_mommy.random_gen import gen_datetime, gen_url
from model_mommy.recipe import Recipe, seq

from badfeed.feeds.models import Entry, Feed


class Command(BaseCommand):
    """CSV data pulled from https://github.com/paiv/fci-breeds."""

    def handle(self, *args, **options):
        Feed.objects.all().delete()
        filepath = os.path.join(os.path.dirname(__file__), "dog-breeds.csv")
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile)
            breeds = [row[1].lower().title() for row in reader]
            random.shuffle(breeds)

        feed_recipe = Recipe(Feed, link=seq(gen_url()), title=itertools.cycle(breeds))
        entry_recipe = Recipe(
            Entry,
            title=itertools.cycle(breeds),
            link=gen_url(),
            date_published=gen_datetime(),
        )
        for i in range(100):
            dog = feed_recipe.make()
            for x in range(random.randint(0, 20)):
                entry_recipe.make(feed=dog)
