import model_utils
from django.db import models
from model_utils.models import TimeStampedModel

FOOD_TYPE_CHOICES = model_utils.Choices(
    (10, 'meat', 'Meat'),
    (11, 'vegetarian', 'Vegetarian'),
    (12, 'vegan', 'Vegan'),
    (100, 'unknown', 'Unknown'),
)


class MenuCard(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)


class Dish(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(default="", max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu_card = models.ForeignKey(
        MenuCard, on_delete=models.SET_NULL, null=True, related_name='dishes'
    )
    prep_time = models.DurationField()
    food_type = models.SmallIntegerField(
        choices=FOOD_TYPE_CHOICES,
        default=10,
        blank=True,
        help_text="Type of food",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'menu_card'], name='unique_dish_name'
            )
        ]

    def __str__(self):
        return self.name
