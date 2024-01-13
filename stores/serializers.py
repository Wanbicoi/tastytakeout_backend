from rest_framework import serializers

from foods.models import Food

from .models import Store


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class GetStoreSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    likers_count = serializers.SerializerMethodField()
    foods = FoodSerializer(many=True)

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None

        if user and user.is_authenticated:
            return obj.likers.filter(id=user.id).exists()
        return False

    def get_likers_count(self, obj):
        return obj.likers.count()

    class Meta:
        model = Store
        fields = [
            "id",
            "owner",
            "name",
            "image_url",
            "address",
            "is_liked",
            "likers_count",
            "foods",
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "owner", "name", "image_url", "address"]


class LikeStoreSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['license_image_url', 'owner_name', 'note']


class TimeStatisticSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()


class FrequencyStatisticSerializer(serializers.Serializer):
    FREQUENCY_CHOICES = [
        ('day', 'day'),
        ('month', 'month'),
        ('year', 'year'),
    ]
    
    frequency = serializers.ChoiceField(choices=FREQUENCY_CHOICES)