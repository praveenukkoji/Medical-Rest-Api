# Generated by Django 3.2.3 on 2021-05-28 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.TextField(primary_key=True, serialize=False)),
                ('user_name', models.TextField()),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_password', models.TextField()),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.role')),
            ],
        ),
    ]
