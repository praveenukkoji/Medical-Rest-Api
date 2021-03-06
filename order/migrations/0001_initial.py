# Generated by Django 3.2.3 on 2021-05-30 08:07

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0002_userstore'),
        ('medicine', '0003_alter_storemedicine_price'),
        ('user', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.TextField(primary_key=True, serialize=False)),
                ('order_datetime', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 8, 7, 47, 158254, tzinfo=utc))),
                ('order_fulfilment_datetime', models.DateTimeField(blank=True)),
                ('order_fulfilment_status', models.TextField(default='pending')),
                ('total_amount', models.FloatField()),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicine.medicine')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
            options={
                'unique_together': {('order_id', 'medicine_id')},
            },
        ),
    ]
