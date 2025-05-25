from rest_framework import serializers
from inventory.models.cart import Cart
from inventory.models.cart_item import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'drug', 'quantity']

    def create(self, validated_data):
        cart = self.context.get('cart')
        return CartItem.objects.create(cart=cart, **validated_data)

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = CartItemSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
