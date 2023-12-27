from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from rest_framework import generics, mixins
from django.contrib.auth import authenticate
from .serializers import LoginUserSerializer, ProfileSerializer, RegisterUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


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


@extend_schema(request=RegisterUserSerializer)
@api_view(["POST"])
def account_registration(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=LoginUserSerializer)
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
