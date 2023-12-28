from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status

from utils.permissions import IsSeller

from .models import Store
from .serializers import GetStoreSerializer, LikeStoreSerializer, StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetStoreSerializer
        else:
            return StoreSerializer

    @extend_schema(request=LikeStoreSerializer)
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        store = self.get_object()
        serializer = LikeStoreSerializer(data=request.data)
        if serializer.is_valid():
            is_liked = serializer.data.get("is_liked", False)  # type: ignore
            if is_liked:
                store.likers.add(request.user)
            else:
                store.likers.remove(request.user)
            store.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
