from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Action, Door

class ActionCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects)
    door = serializers.PrimaryKeyRelatedField(queryset=Door.objects)

    class Meta:
        model = Action
        exclude = ['created', 'id']

class DoorCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = Door
        exclude = ['created', 'id', 'history', 'is_open']


class DoorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = '__all__'