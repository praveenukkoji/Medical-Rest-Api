# Generated by Django 3.2.3 on 2021-06-14 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('view_id', models.TextField(primary_key=True, serialize=False)),
                ('view_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.role')),
                ('view_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.view')),
            ],
            options={
                'unique_together': {('role_id', 'view_id')},
            },
        ),
    ]
