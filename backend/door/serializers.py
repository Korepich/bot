from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Action, Door, Breaking


# Action
class ActionCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects)
    door = serializers.PrimaryKeyRelatedField(queryset=Door.objects)

    class Meta:
        model = Action
        exclude = ["created", "id"]


class ActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        exclude = ["user", "door"]


# Breaking
class BreakingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breaking
        fields = "__all__"


class BreakingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breaking
        fields = "__all__"


# Door
class DoorCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = Door
        exclude = ["created", "id", "history", "is_open"]


class DoorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = "__all__"
