from django.db import models
from django.contrib.auth.models import User
from datetime import date


class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    added_on = models.DateField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        return self.expiration_date < date.today()

    def __str__(self):
        return f"{self.name} - {self.quantity} - {self.expiration_date}"
