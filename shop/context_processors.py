from .utils import cart_count, cart_total


def cart_summary(request):
    return {"cart_count": cart_count(request), "cart_total": cart_total(request)}
