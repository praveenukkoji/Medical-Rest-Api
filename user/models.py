from django.db import models


class Role(models.Model):
    role_id = models.TextField(primary_key=True)
    role_type = models.TextField(unique=True)


class User(models.Model):
    user_id = models.TextField(primary_key=True)
    user_name = models.TextField()
    user_email = models.EmailField(unique=True)
    user_password = models.TextField()
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

