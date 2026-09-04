from django.shortcuts import get_object_or_404
from mcp_server import ModelQueryToolset, MCPToolset
from sale.models import Cart, CartItem, Order, OrderItem


class CartQueryTool(ModelQueryToolset):
    model = Cart

class CartItemQueryTool(ModelQueryToolset):
    model = CartItem

class OrderQueryTool(ModelQueryToolset):
    model = Order

class OrderItemQueryTool(ModelQueryToolset):
    model = OrderItem

class CheckoutCartMCPTool(MCPToolset):
    def do_checkout_cart(self, cart_id: str = None, email: str= None, shipping_address: str=None):
        """
        Checkout the cart to remove all CartItem from Cart.
        And create new Order with OrderItem with duplicaing the items from CartItem
        """
        cart = get_object_or_404(Cart, id=cart_id)
        if cart.items.count() == 0:
            return {"status": "Error, the cart has no item"}
        else:
            cart.checkout(email=email, shipping_address=shipping_address)
            return {"status": "Successfully checkout the cart"}

