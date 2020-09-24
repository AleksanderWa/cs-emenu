from django.db import models
from model_utils.models import TimeStampedModel

FOOD_TYPE_CHOICES = ((10, "Meat"), (11, "Vegetarian"), (12, "Vegan"))


class Dish(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    prep_time = models.DurationField()
    food_type = models.SmallIntegerField(
        choices=FOOD_TYPE_CHOICES, default=10, blank=True, help_text="Type of food"
    )

    def __str__(self):
        return self.name


class MenuCard(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)
