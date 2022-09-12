import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates many lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many lists do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created_lists = seeder.execute()
        created_clean = flatten(list(created_lists.values()))
        for pk in created_clean:
            obj = list_models.List.objects.get(pk=pk)
            # Seed Rooms
            for r in rooms:
                magic_number = random.randint(1, 15)
                if magic_number % 3 == 0:
                    obj.rooms.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} list(s) created!!"))
