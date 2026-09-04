from rest_framework import serializers
from sale.models import CartItem, Cart, Order


class AddCartItemSerializer(serializers.ModelSerializer):
    total_item = serializers.IntegerField(source="cart.total_item", read_only=True)
    total_price = serializers.DecimalField(source="cart.total_price", read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total_item', 'total_price']


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source='product.image', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['product_id', 'image', 'name', 'price', 'quantity']


class CartDetailSerializer(serializers.ModelSerializer):
    total_item = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'


class SubmitPaymentSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
        cart = self.context['request'].user.member.cart
        return cart.checkout(
            email=validated_data['email'],
            shipping_address=validated_data['shipping_address'],
            slip_image=validated_data.get('slip_image'),
        )

  class Meta:
        model = Order
        exclude = ['cart']

