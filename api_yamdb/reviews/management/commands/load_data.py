import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title,)
from users.models import User

TABLES = {
    User: 'users.csv',
    Comment: 'comments.csv',
    Review: 'review.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, dir in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{dir}',
                'r',
                encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)
                model.objects.bulk_create(model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
