from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from carts.models import Cart
from carts.serializers import CartSerializer, GetCartSerializer


class CartViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ViewSetMixin,
    GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetCartSerializer
        else:
            return CartSerializer

    def get_queryset(self):  # type: ignore
        return Cart.objects.filter(buyer=self.request.user)
