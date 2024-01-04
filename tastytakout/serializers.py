from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from stores.models import Store


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role  # type: ignore
        if str(user.role) == "SELLER":  # type: ignore
            try:
                token["store_id"] = Store.objects.filter(owner=user).first().id  # type: ignore
            except Store.DoesNotExist:
                token["store_id"] = None
        return token
