from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from foods.filters import FoodFilter
from .models import Category, Food, FoodComment
from .serializers import (
    CategorySerializer,
    FoodSerializer,
    FoodCommentSerializer,
    GetFoodSerializer,
)
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FoodFilter

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetFoodSerializer
        else:
            return FoodSerializer

    # def list(self, request):
    #     queryset = Food.objects.all()
    #     serializer = Food(queryset, many=True)
    #     return Response(serializer.data)

    @extend_schema(request=FoodCommentSerializer)
    @action(detail=True, methods=["post", "delete"])
    def comment(self, request, pk=None):
        food = self.get_object()
        if request.method == "POST":
            serializer = FoodCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(food=food, commenter=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            comment_id = request.data.get("comment_id")
            try:
                comment = FoodComment.objects.get(id=comment_id, food=food)
                comment.delete()
                return Response(
                    {"detail": "Comment deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except FoodComment.DoesNotExist:
                return Response(
                    {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"detail": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
