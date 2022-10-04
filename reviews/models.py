from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    RATING_VERY_GOOD = 5
    RATING_GOOD = 4
    RATING_AVERAGE = 3
    RATING_BAD = 2
    RATING_VERY_BAD = 1

    RATING_CHOICES = (
        (RATING_VERY_GOOD, "Very Good"),
        (RATING_GOOD, "Good"),
        (RATING_AVERAGE, "Average"),
        (RATING_BAD, "Bad"),
        (RATING_VERY_BAD, "Very Bad"),
    )

    review = models.CharField(max_length=500)
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self) -> str:
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    class Meta:
        ordering = ("-created_at",)
