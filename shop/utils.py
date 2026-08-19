from decimal import Decimal

from .models import Product


def get_cart(request):
    return request.session.get("cart", {})


def cart_count(request):
    return sum(int(quantity) for quantity in get_cart(request).values())


def cart_items(request):
    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart.keys()).select_related("category")
    items = []
    for product in products:
        quantity = min(int(cart.get(str(product.id), 0)), product.stock)
        if quantity > 0:
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": product.price * quantity,
            })
    return items


def cart_total(request):
    return sum((item["subtotal"] for item in cart_items(request)), Decimal("0.00"))
