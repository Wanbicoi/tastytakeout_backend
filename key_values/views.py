from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from foods.models import Food
from orders.models import Voucher
from key_values.models import KeyValues
from key_values.serializers import GetHomeDataSerializer, HomeDataSerializer


@extend_schema(request=HomeDataSerializer, responses=GetHomeDataSerializer)
@api_view(["GET", "PUT"])
def home_data(request):
    if request.method == "GET":
        home_data = KeyValues.objects.get(key="home").data
        food_ids = home_data.get("foodIds", [])
        voucher_ids = home_data.get("voucherIds", [])

        foods = Food.objects.filter(id__in=food_ids)
        vouchers = Voucher.objects.filter(id__in=voucher_ids)

        home_data["foods"] = foods
        home_data["vouchers"] = vouchers

        serializer = GetHomeDataSerializer(home_data)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = HomeDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        home_data = KeyValues.objects.get(key="home")
        home_data.data = serializer.validated_data
        home_data.save()
        return Response(serializer.validated_data)
