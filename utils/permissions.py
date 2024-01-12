from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.method in SAFE_METHODS) or request.user.role == "SELLER"


class IsBuyer(BasePermission):
    def has_permission(self, request, view):  # type: ignore
<<<<<<< HEAD
        return bool(request.method in SAFE_METHODS) and request.user.role == "BUYER"
    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
=======
        return bool(request.method in SAFE_METHODS) or request.user.role == "BUYER"
>>>>>>> origin/master
