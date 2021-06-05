from django.db import models

from user.models import User


class Store(models.Model):
    store_id = models.TextField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.TextField()
    store_phone_number = models.TextField(unique=True)
    store_address = models.TextField()

