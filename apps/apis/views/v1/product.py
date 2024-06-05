from apis.models import Product, SaleOrder, User
from apis.serializer import ProductSerializer, SaleOrderSerializer

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
        
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated]
        
    def get_queryset(self):
        return self.queryset
    
    def get(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required for product creation'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required for product updates'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_superuser:
            return Response({'error': 'Permission denied: Only superusers can update product stock'}, status=status.HTTP_403_FORBIDDEN)

        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        new_quantity = request.data.get('quantity')
        if new_quantity is None:
            return Response({'error': 'Missing required field: quantity'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                return Response({'error': 'Quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid quantity format: Must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        product.quantity = new_quantity
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class PurchaseProductViewset(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required for order creation'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        product_ids = data.get('product_ids', [])
        quantities = data.get('quantities', [])

        if not product_ids or not quantities:
            return Response({'error': 'Missing required fields: product_ids and quantities'}, status=status.HTTP_400_BAD_REQUEST)

        if len(product_ids) != len(quantities):
            return Response({'error': 'Number of product_ids must match number of quantities'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        for product_id, quantity in zip(product_ids, quantities):
            try:
                product = Product.objects.get(pk=product_id)
                if product.quantity < quantity:
                    return Response({'error': f'Product {product.title} is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

                total_price += product.unit_price * quantity
                product.quantity -= quantity
                product.save()
            except:
                return Response({'error': f'Product with ID {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        sale_order = SaleOrder.objects.create(
            products=Product.objects.filter(id__in=product_ids),
            users=user,
            total_price=total_price
        )

        serializer = SaleOrderSerializer(sale_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SaleOrderViewSet(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer

    def create(self, request):
        user = request.user
        product_ids = request.data.get('product_ids', [])
        quantities = request.data.get('quantities', [])

        if not product_ids or not quantities:
            return Response({'error': 'Missing required fields: product_ids and quantities'}, status=400)
        
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required for order creation'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        product_ids = data.get('product_ids', [])
        quantities = data.get('quantities', [])

        if not product_ids or not quantities:
            return Response({'error': 'Missing required fields: product_ids and quantities'}, status=status.HTTP_400_BAD_REQUEST)

        if len(product_ids) != len(quantities):
            return Response({'error': 'Number of product_ids must match number of quantities'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        for product_id, quantity in zip(product_ids, quantities):
            try:
                product = Product.objects.get(pk=product_id)
                if product.quantity < quantity:
                    return Response({'error': f'Product {product.title} is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

                total_price += product.unit_price * quantity
                product.quantity -= quantity
                product.save()
            except:
                return Response({'error': f'Product with ID {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        sale_order = SaleOrder.objects.create(
            products=Product.objects.filter(id__in=product_ids),
            users=user,
            total_price=total_price
        )

        serializer = SaleOrderSerializer(sale_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
