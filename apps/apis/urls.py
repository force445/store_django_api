from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from apis.views.v1.product import ProductViewSet,PurchaseProductViewset, SaleOrderViewSet

api_v1_urls = ([
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<int:pk>/purchase/', PurchaseProductViewset.as_view({'post': 'create'}), name='product-purchase'),
    path('sale_orders/', SaleOrderViewSet.as_view({'get': 'list'}), name='sale-order-list'),
    path('sale_orders/<int:pk>/', SaleOrderViewSet.as_view({'get': 'retrieve'}), name='sale-order-detail'),
])

urlpatterns = [
    path('v1/', include(api_v1_urls)),
]
