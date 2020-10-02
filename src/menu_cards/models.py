import model_utils
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from rest_framework.authtoken.models import Token

FOOD_TYPE_CHOICES = model_utils.Choices(
    (10, "meat", "Meat"),
    (11, "vegetarian", "Vegetarian"),
    (12, "vegan", "Vegan"),
    (100, "unknown", "Unknown"),
)


class MenuCard(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)


class Dish(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(default="", max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu_card = models.ForeignKey(
        MenuCard, on_delete=models.SET_NULL, null=True, related_name="dishes"
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
                fields=["name", "menu_card"], name="unique_dish_name"
            )
        ]

    def __str__(self):
        return self.name

    @property
    def is_vegetarian(self):
        return (
            self.food_type == FOOD_TYPE_CHOICES.vegetarian
            or self.food_type == FOOD_TYPE_CHOICES.vegan
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class DishPhoto(TimeStampedModel):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(
        upload_to="photo",
        validators=[
            FileExtensionValidator(
                ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "gif", "GIF"]
            )
        ],
    )
