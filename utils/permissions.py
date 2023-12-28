from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.method in SAFE_METHODS) and request.user.role == "SELLER"


class IsBuyer(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.method in SAFE_METHODS) and request.user.role == "BUYER"
