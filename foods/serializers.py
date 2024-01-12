from rest_framework import serializers

from stores.serializers import StoreSerializer
from .models import Category, Food, FoodComment, FoodDiscount


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FoodCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComment
        fields = ["content", "rating"]


class FoodDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDiscount
        fields = "__all__"


class GetFoodSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    likers_count = serializers.SerializerMethodField()
    category = CategorySerializer()
    store = StoreSerializer()
    comments = FoodCommentSerializer(many=True)  
    
    is_liked = serializers.SerializerMethodField()
    likers_count = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None

        if user and user.is_authenticated:
            return obj.likers.filter(id=user.id).exists()
        return False

    def get_likers_count(self, obj):
        return obj.likers.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None

        if user and user.is_authenticated:
            return obj.likers.filter(id=user.id).exists()
        return False

    def get_likers_count(self, obj):
        return obj.likers.count()

    class Meta:
        model = Food
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"
        # exclude = ("store", "category")


class LikeFoodSerializer(serializers.Serializer):
<<<<<<< HEAD
    is_liked = serializers.BooleanField()
=======
    is_liked = serializers.BooleanField()
>>>>>>> origin/master
