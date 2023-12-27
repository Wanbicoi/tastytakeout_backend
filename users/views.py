from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from rest_framework import generics, mixins
from django.contrib.auth import authenticate
from .serializers import LoginUserSerializer, ProfileSerializer, RegisterUserSerializer
from foods.models import Food
from .serializers import UserLikeFoodSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ViewSetMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(method="post", request_body=RegisterUserSerializer)
@api_view(["POST"])
def account_registration(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", request_body=LoginUserSerializer)
@api_view(["POST"])
def account_login(request):
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get("username")  # type: ignore
        password = serializer.data.get("password")  # type: ignore

        user = authenticate(username=username, password=password)
        print((username, password))
        if user is not None:
            jwt_token = RefreshToken.for_user(user)
            return Response(
                {"user": serializer.data, "token": str(jwt_token.access_token)},  # type: ignore
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"messages": "Please check your email or password!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get favorite foods of a user
# /users/20/favorite-foods/
@api_view(["GET"])
def get_favorite_foods(request, user_id):
    try:       
        user = User.objects.get(id=user_id)
        serialized_foods = UserLikeFoodSerializer(user).data
        return Response(serialized_foods, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    

# Check if a user likes a food
# /users/check-user-likes-food/?user_id=16&food_id=5
@api_view(["GET"])
def check_user_likes_food(request):
    user_id = request.query_params.get('user_id')
    food_id = request.query_params.get('food_id')

    try:
        user = User.objects.get(id=user_id)
        food = Food.objects.get(id=food_id)

        if food in user.liked_foods.all():
            return Response({"user_likes_food": True}, status=status.HTTP_200_OK)
        else:
            return Response({"user_likes_food": False}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    except Food.DoesNotExist:
        return Response({"message": "Food does not exist"}, status=status.HTTP_404_NOT_FOUND)
