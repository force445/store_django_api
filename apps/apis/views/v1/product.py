from rest_framework import viewsets
from apis.models import Product
from apis.serializer import ProductSerializer


class ProductViewset(viewsets.ModelViewSet):
    def get(self, request):
        