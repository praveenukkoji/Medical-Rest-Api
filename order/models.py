from django.db import models

from user.models import User
from store.models import Store
from medicine.models import Medicine


class Order(models.Model):
    order_id = models.TextField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_datetime = models.DateTimeField()
    order_fulfilment_datetime = models.DateTimeField(null=True)
    order_fulfilment_status = models.TextField(default="pending")
    total_amount = models.FloatField()


class OrderMedicine(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    order_quantity = models.IntegerField()

    class Meta:
        unique_together = (('order_id', 'medicine_id'),)
