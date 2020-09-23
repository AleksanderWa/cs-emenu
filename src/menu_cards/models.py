from django.db import models

FOOD_TYPE_CHOICES = ((10, "Meat"), (11, "Vegetarian"), (12, "Vegan"))


class TimeManager(models.Model):
    creation_date = models.TimeField(auto_now=True)
    last_update = models.TimeField(default=creation_date)


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    prep_time = models.DurationField()
    time_stamps = models.ForeignKey(TimeManager, on_delete=models.CASCADE, null=True)
    food_type = models.SmallIntegerField(
        choices=FOOD_TYPE_CHOICES, default=10, blank=True, help_text="Type of food"
    )

    def __str__(self):
        return self.name


class MenuCard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(default="", max_length=250)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)
    time_stamps = models.ForeignKey(TimeManager, on_delete=models.CASCADE, null=True)
