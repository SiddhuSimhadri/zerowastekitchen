from django.db import models
from django.contrib.auth.models import User

class WasteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    wasted_on = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=100, choices=(
        ('expired', 'Expired'),
        ('spoiled', 'Spoiled'),
        ('forgotten', 'Forgotten'),
    ))

    def __str__(self):
        return f"{self.item_name} wasted on {self.wasted_on} due to {self.reason}"
