from django.db import models

from store.models import Store


class Medicine(models.Model):
    medicine_id = models.TextField(primary_key=True)
    medicine_name = models.TextField(unique=True)


class StoreMedicine(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = (('store_id', 'medicine_id'),)
