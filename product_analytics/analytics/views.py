from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
