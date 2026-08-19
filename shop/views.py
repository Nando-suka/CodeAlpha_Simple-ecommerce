from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegisterForm
from .models import Category, Order, OrderItem, Product
from .utils import cart_items, cart_total, get_cart


def home(request):
    products = Product.objects.select_related("category").all()
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    if selected_category:
        products = products.filter(category__slug=selected_category)
    return render(request, "shop/home.html", {
        "products": products,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": selected_category,
        "featured_products": Product.objects.filter(featured=True).select_related("category")[:4],
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, "shop/product_detail.html", {"product": product, "related_products": related_products})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to Northstar Market. Your account is ready.")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})


def cart(request):
    return render(request, "shop/cart.html", {"items": cart_items(request), "cart_total": cart_total(request)})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method != "POST":
        return redirect(product.get_absolute_url())
    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        quantity = 1
    cart_data = get_cart(request)
    current = int(cart_data.get(str(product.id), 0))
    if not product.is_in_stock:
        messages.error(request, "This product is currently out of stock.")
    else:
        cart_data[str(product.id)] = min(current + quantity, product.stock)
        request.session["cart"] = cart_data
        request.session.modified = True
        messages.success(request, f"{product.name} was added to your cart.")
    return redirect(request.POST.get("next") or "cart")


def cart_update(request):
    if request.method == "POST":
        cart_data = get_cart(request)
        for key, value in request.POST.items():
            if not key.startswith("quantity_"):
                continue
            product_id = key.replace("quantity_", "", 1)
            try:
                quantity = max(0, int(value))
            except (TypeError, ValueError):
                quantity = 1
            product = Product.objects.filter(pk=product_id).first()
            if product and quantity:
                cart_data[product_id] = min(quantity, product.stock)
            else:
                cart_data.pop(product_id, None)
        request.session["cart"] = cart_data
        request.session.modified = True
        messages.success(request, "Your cart has been updated.")
    return redirect("cart")


def cart_remove(request, product_id):
    if request.method == "POST":
        cart_data = get_cart(request)
        cart_data.pop(str(product_id), None)
        request.session["cart"] = cart_data
        request.session.modified = True
        messages.success(request, "Item removed from your cart.")
    return redirect("cart")


@login_required
def checkout(request):
    items = cart_items(request)
    if not items:
        messages.info(request, "Add something to your cart before checking out.")
        return redirect("home")
    initial = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
    }
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            locked_products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(id__in=[item["product"].id for item in items])
            }
            total = Decimal("0.00")
            order = Order.objects.create(user=request.user, **form.cleaned_data)
            for item in items:
                product = locked_products.get(item["product"].id)
                quantity = item["quantity"]
                if not product or product.stock < quantity:
                    messages.error(request, f"{item['product'].name} no longer has enough stock.")
                    return redirect("cart")
                subtotal = product.price * quantity
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=quantity,
                    subtotal=subtotal,
                )
                product.stock -= quantity
                product.save(update_fields=["stock", "updated_at"])
                total += subtotal
            order.total = total
            order.save(update_fields=["total"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} placed successfully.")
        return redirect("order_success", order_id=order.pk)
    return render(request, "shop/checkout.html", {"form": form, "items": items, "cart_total": cart_total(request)})


@login_required
def orders(request):
    return render(request, "shop/orders.html", {"orders": request.user.orders.prefetch_related("items").all()})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related("items"), pk=order_id)
    return render(request, "shop/order_success.html", {"order": order})
