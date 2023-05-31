from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField()
    is_thief = models.BooleanField(default=False)
    door = models.ForeignKey('door.Door', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Door(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(unique=True, max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=False)
    history = models.ManyToManyField(Action, related_name="+")

    def __str__(self):
        return self.name
