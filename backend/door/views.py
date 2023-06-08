from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Action, Door, Breaking
from .serializers import (
    DoorCreateSerializer,
    DoorRetrieveSerializer,
    ActionCreateSerializer,
    ActionListSerializer,
    BreakingCreateSerializer,
    BreakingListSerializer,
)
from .pagination import ActionPagination
from helpers.serializer_lifecycle import serializer_lifecycle
from helpers.get_data_with_user import get_data_with_user


# Action
class ActionCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Action.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ActionCreateSerializer

    def create(self, request):
        data = get_data_with_user(request, "user")

        serializer = serializer_lifecycle(self.serializer_class, data=data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActionListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionListSerializer
    pagination_class = ActionPagination

    def get_queryset(self):
        return self.queryset.order_by("-created")


# Breaking
class BreakingCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Breaking.objects.all()
    serializer_class = BreakingCreateSerializer


class BreakingListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Breaking.objects.all()
    serializer_class = BreakingListSerializer
    pagination_class = ActionPagination

    def get_queryset(self):
        return self.queryset.order_by("-created")


# Door
class DoorRetrieveView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Door.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DoorRetrieveSerializer

    def retrieve(self, request, pk):
        serializer = self.serializer_class(self.queryset.get(pk=pk))

        return Response(serializer.data, status=status.HTTP_200_OK)


class DoorListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Door.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DoorRetrieveSerializer

    def list(self, request):
        serializer = self.serializer_class(
            self.get_queryset().filter(owner=request.user), many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class DoorCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Door.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DoorCreateSerializer

    def create(self, request):
        data = get_data_with_user(request, "owner")

        serializer = serializer_lifecycle(DoorCreateSerializer, data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
