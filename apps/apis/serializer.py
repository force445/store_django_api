from rest_framework import serializers
from apis.models import User, Product, SaleOrder

class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data["deleted"]
        del data["deleted_by_cascade"]
        return data

    class Meta:
        model = User
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data["deleted"]
        del data["deleted_by_cascade"]
        return data
    
    class Meta:
        model = Product
        fields = "__all__"

class SaleOrderSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data["deleted"]
        del data["deleted_by_cascade"]
        data['product'] = ProductSerializer(instance.product).data
        data['User'] = UserSerializer(instance.product).data
        return data
    
    class Meta:
        model = SaleOrder
        fields = "__all__"