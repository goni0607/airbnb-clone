from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command create base code for rules of house"

    def handle(self, *args, **options):
        houserules = [
            "No smoking",
            "No parties or events",
            "Pets are allowed",
            "No Pets",
            "Not suitable for children and infants",
        ]

        room_models.HouseRule.objects.all().delete()
        for r in houserules:
            room_models.HouseRule.objects.create(name=r)
        self.stdout.write(self.style.SUCCESS("Rules of house created!!"))
