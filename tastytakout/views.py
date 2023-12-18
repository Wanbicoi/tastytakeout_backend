from rest_framework import viewsets
from .models import (
    User,
    Cart,
    Category,
    Food,
    FoodComment,
    Store,
    Order,
    OrderFood,
    BuyerLikeFood,
    BuyerLikeStore,
    Voucher,
    FoodDiscount,
    Chat,
)
from .serializers import (
    UserSerializer,
    CartSerializer,
    CategorySerializer,
    FoodSerializer,
    FoodCommentSerializer,
    StoreSerializer,
    OrderSerializer,
    OrderFoodSerializer,
    BuyerLikeFoodSerializer,
    BuyerLikeStoreSerializer,
    VoucherSerializer,
    FoodDiscountSerializer,
    ChatSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodCommentViewSet(viewsets.ModelViewSet):
    queryset = FoodComment.objects.all()
    serializer_class = FoodCommentSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderFoodViewSet(viewsets.ModelViewSet):
    queryset = OrderFood.objects.all()
    serializer_class = OrderFoodSerializer


class BuyerLikeFoodViewSet(viewsets.ModelViewSet):
    queryset = BuyerLikeFood.objects.all()
    serializer_class = BuyerLikeFoodSerializer


class BuyerLikeStoreViewSet(viewsets.ModelViewSet):
    queryset = BuyerLikeStore.objects.all()
    serializer_class = BuyerLikeStoreSerializer


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer


class FoodDiscountViewSet(viewsets.ModelViewSet):
    queryset = FoodDiscount.objects.all()
    serializer_class = FoodDiscountSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
