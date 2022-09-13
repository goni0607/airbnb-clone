from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command create base code for type of rooms"

    def handle(self, *args, **options):
        room_types = [
            "Entire place",
            "Hotel room",
            "Private room",
            "Shared room",
        ]

        room_models.RoomType.objects.all().delete()
        for r in room_types:
            room_models.RoomType.objects.create(name=r)
        self.stdout.write(self.style.SUCCESS("Type of rooms created!!"))
