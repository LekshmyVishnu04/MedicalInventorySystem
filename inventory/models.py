from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Inventory(models.Model):

    medicinename = models.CharField(max_length=20)
    availablestock = models.IntegerField()
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
