from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Voucher
from .serializers import VoucherSerializer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.db.models import F

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

@api_view(["GET"])
def count_valid_vouchers(request):
    current_datetime = timezone.now()
    valid_vouchers_count = Voucher.objects.filter(end__gte=current_datetime,used_quantity__lt=F('quantity')).count()
    
    return Response({"valid_vouchers_count": valid_vouchers_count}, status=200)
