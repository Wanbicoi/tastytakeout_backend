from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ViewSetMixin,
    GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):  # type: ignore
        return (
            Notification.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by(
                "-created_at",
            )
        )
