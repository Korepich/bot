from django.db import models
from django.contrib.auth.models import User


class Action(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField()
    door = models.ForeignKey("door.Door", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.created.strftime("%m/%d/%Y, %H:%M:%S")


class Breaking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    door = models.ForeignKey("door.Door", on_delete=models.CASCADE)

    def __str__(self):
        return self.created.strftime("%m/%d/%Y, %H:%M:%S")


class Door(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(unique=True, max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=False)
    history = models.ManyToManyField(Action, related_name="+")
    breaking_history = models.ManyToManyField(Breaking, related_name="+")

    def __str__(self):
        return self.name
