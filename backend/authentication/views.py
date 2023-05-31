from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import UserCreateSerializer
from helpers.serializer_lifecycle import serializer_lifecycle

class UserCreateView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = serializer_lifecycle(self.serializer_class, data=request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)