from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ChangePasswordSerializer,
    LoginUserSerializer,
    ProfileSerializer,
    RegisterUserSerializer,
)


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


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)

            # Return a success response
            return Response({"message": "Profile updated successfully."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check the old password
            old_password = serializer.validated_data["old_password"]
            if not user.check_password(old_password):
                return Response(
                    {"detail": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the new password and save the user
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
