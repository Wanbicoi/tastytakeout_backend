from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status

from utils.permissions import IsSeller, IsOwner

from .models import Store
from .serializers import GetStoreSerializer, LikeStoreSerializer, StoreSerializer, VerificationSerializer, TimeStatisticSerializer, FrequencyStatisticSerializer
from django_filters import rest_framework as filters
from stores.filters import StoreFilter

from datetime import datetime, timedelta

from orders.models import Order, OrderFood
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, Coalesce
from django.db.models import Sum, Count, F, DecimalField

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StoreFilter

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetStoreSerializer
        else:
            return StoreSerializer

    @extend_schema(request=LikeStoreSerializer)
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        store = self.get_object()
        serializer = LikeStoreSerializer(data=request.data)
        if serializer.is_valid():
            is_liked = serializer.data.get("is_liked", False)  # type: ignore
            if is_liked:
                store.likers.add(request.user)
            else:
                store.likers.remove(request.user)
            store.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    filter_backends = (filters.DjangoFilterBackend,)

    @extend_schema(request=VerificationSerializer)
    @action(detail=True, methods=["post"])
    def request_verification(self, request, pk=None):
        store = self.get_object()
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            owner_name = serializer.data.get("owner_name")  # type: ignore
            license_image_url = serializer.data.get("license_image_url")
            note = serializer.data.get("note")
            if owner_name and license_image_url:
                store.owner_name = owner_name
                store.license_image_url = license_image_url
                store.note = note
                store.created_at = datetime.datetime.now()
                store.status = "PENDING"
            store.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    @extend_schema(request=FrequencyStatisticSerializer)
    @action(detail=True, methods=["post"])
    def get_revenue(self, request, pk=None):
        try:            
            serializer = FrequencyStatisticSerializer(data=request.data)
            if serializer.is_valid():
                frequency = serializer.data.get("frequency", False)
                if frequency not in ['day', 'month', 'year']:
                    return Response({'error': 'Invalid frequency'}, status=status.HTTP_400_BAD_REQUEST)
                
                store = self.get_object()                
                today = datetime.now().date()

                if frequency == 'day':
                    date_field = TruncDate('created_at')
                    max_interval = 100
                    interval_unit = 'days'
                elif frequency == 'month':
                    date_field = TruncMonth('created_at')
                    max_interval = 24*4
                    interval_unit = 'weeks'
                elif frequency == 'year':
                    date_field = TruncYear('created_at')
                    max_interval = 10*12*4
                    interval_unit = 'weeks'

                start_date = today - timedelta(**{interval_unit: max_interval})

                orders = Order.objects.filter(store=store.pk,status='COMPLETED')
                revenue_data = orders.filter(created_at__gte=start_date
                                            ).annotate(truncated_date=date_field
                                            ).values('truncated_date').annotate(
                                                total_revenue=Sum('total')
                                            ).order_by('truncated_date')

                
                response_data = {
                    'result': 'Success',
                    'revenue_data': list(revenue_data)
                }

                return Response(response_data)      
              
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)})

    @extend_schema(request=TimeStatisticSerializer)
    @action(detail=True, methods=["post"])
    def get_best_sellings(self, request, pk=None):
        try:
            serializer = TimeStatisticSerializer(data=request.data)
            if serializer.is_valid():
                store = self.get_object()

                month = serializer.data.get('month')
                year = serializer.data.get('year')

                orders = Order.objects.filter(store=store.pk,created_at__month=month, created_at__year=year,status='COMPLETED')
                order_foods = OrderFood.objects.filter(order__in=orders)
                
                # Aggregate sales quantity for each food
                sales_data = (order_foods.values('food','food__name')
                                        .annotate(
                                            total_sales=Coalesce(Sum('quantity'), 0),
                                            revenue=Coalesce(Sum(F('quantity') * F('food__price')), 0, output_field=DecimalField())
                                        )
                                        .order_by('-total_sales')[:5])
                
                response_data = {
                    'result': 'Success',
                    'best_sellings': [
                        {
                            'food_name': item['food__name'],
                            'total_sales': item['total_sales'],
                            'revenue': item['revenue']
                        }
                        for item in sales_data
                    ]
                }
                return Response(response_data)      
              
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)})

