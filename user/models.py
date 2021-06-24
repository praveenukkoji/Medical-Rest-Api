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


class View(models.Model):
    view_id = models.TextField(primary_key=True)
    view_name = models.TextField(unique=True)


class Authorization(models.Model):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    view_id = models.ForeignKey(View, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('role_id', 'view_id'),)
