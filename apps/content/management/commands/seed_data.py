import csv
import random
from datetime import datetime, timedelta
import pytz
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils import timezone
from django_seed import Seed
import logging


User = get_user_model()
Profile = apps.get_model("users", "Profile")
Genre = apps.get_model("music", "Genre")
RecordLabel = apps.get_model("music", "RecordLabel")
Playlist = apps.get_model("music", "Playlist")
Album = apps.get_model("music", "Album")
Artist = apps.get_model("music", "Artist")
Song = apps.get_model("music", "Song")
SongPlayLog = apps.get_model("music", "SongPlayLog")
City = apps.get_model("content", "City")

DEFAULT_START_DATE = datetime(2022, 1, 1, tzinfo=pytz.UTC)
DEFAULT_END_DATE = timezone.now()

def random_date(start=DEFAULT_START_DATE, end=DEFAULT_END_DATE):
    """
    This function will return a random datetime between two datetime
    objects.
    """

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


class Command(BaseCommand):
    """seed_data command"""

    help = "Makes the current database have the same data as the fixture(s), no more, no less."
    args = "fixture [fixture ...]"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--skip-remove",
            action="store_false",
            dest="remove",
            default=True,
            help="Avoid remove any object from db",
        )
        parser.add_argument(
            "--remove-before",
            action="store_true",
            dest="remove_before",
            default=False,
            help="Remove existing objects before inserting and updating new ones",
        )

    def handle(self, *args, **options):
        self.style = no_style()
        try:
            self.seed_data()
        except Exception as exc:
            raise CommandError(exc)

    def seed_data(self):
        logging.getLogger().setLevel(logging.CRITICAL)  # squelch django-seed bugginess

        # populate city, state data
        self.stdout.write("Populating city location data...")
        with open("setup/cities.csv", newline="") as csvfile:
            rows = csv.reader(csvfile, delimiter=",")
            next(rows)

            city_objs = []
            for row in rows:
                state, name, lat, long = row
                city_objs.append(City(state=state, name=name, latitude=lat, longitude=long))

            City.objects.bulk_create(city_objs, ignore_conflicts=True)

        if not User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists():
            self.stdout.write("Creating superuser...")
            User.objects.create_superuser(settings.DJANGO_SUPERUSER_USERNAME, settings.DJANGO_SUPERUSER_EMAIL, settings.DJANGO_SUPERUSER_PASSWORD)

        seeder = Seed.seeder()

        # populate user data
        self.stdout.write("Populating users and user profiles...")
        seeder.add_entity(User, 100)
        seeder.add_entity(Profile, 100)

        # populate artist/song data
        self.stdout.write("Populating genres...")
        Genre.objects.bulk_create([Genre(name=g) for g in list(dict(Genre.GENRE_CHOICES).keys())], ignore_conflicts=True)

        self.stdout.write("Populating Record labels, artist, album, playlist, and song data...")
        seeder.add_entity(
            RecordLabel,
            10,
            {
                "name": lambda x: seeder.faker.company(),
            },
        )
        seeder.add_entity(
            Artist,
            200,
            {"name": lambda x: seeder.faker.name()},
        )
        # artists = Artist.objects.all()
        seeder.add_entity(
            Album,
            300,
            {
                "name": lambda x: seeder.faker.sentence(),
            },
        )
        seeder.add_entity(
            Song,
            1000,
            {
                "name": lambda x: seeder.faker.sentence(),
                # "artists": lambda x: random.choice(artists),
            },
        )
        seeder.add_entity(
            Playlist,
            250,
            {
                "name": lambda x: f"{seeder.faker.name()}'s Playlist",
            },
        )

        # populate song play logs
        self.stdout.write("Populating playtime song logs. This could take a few minutes...")
        seeder.add_entity(
            SongPlayLog,
            random.randint(7777, 9999),
            {"date_played": lambda x: random_date()}
        )

        seeder.execute()

        logging.getLogger().setLevel(logging.INFO)  # squelch django-seed bugginess
