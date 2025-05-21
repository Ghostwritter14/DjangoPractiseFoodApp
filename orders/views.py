import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import base64
import io

from django.views.decorators.http import require_POST

from food.models import CustomCombo, Item
from orders.models import Order, OrderItem


# Create your views here.
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart = request.session.get('cart', {})

    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart

    messages.success(request, f"Added {item.item_name} to cart.")

    return redirect(request.META.get('HTTP_REFERER', 'food:index'))


@login_required
def add_combo_to_cart(request, combo_id):
    combo = get_object_or_404(CustomCombo, pk=combo_id, user=request.user)
    cart = request.session.get('cart', {})

    for itm in combo.items.all():
        key = str(itm.id)
        cart[key] = cart.get(key, 0) + 1

    request.session['cart'] = cart
    messages.success(request, f"Added combo “{combo.name}” to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'profile'))


@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for id_str, qty in cart.items():
        item = get_object_or_404(Item, pk=int(id_str))
        subtotal = item.item_price * qty
        items.append({
            'item': item,
            'quantity': qty,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'orders/cart.html', {
        'cart_items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        messages.success(request, "Removed item from cart.")
    return redirect('orders:cart_detail')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    return render(request, 'orders/order_detail.html', {
        'order': order
    })


@login_required
@require_POST
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('orders:cart_detail')

    order = Order.objects.create(user=request.user)
    for id_str, qty in cart.items():
        item = get_object_or_404(Item, pk=int(id_str))
        OrderItem.objects.create(order=order, item=item, quantity=qty)

    request.session['cart'] = {}
    messages.success(request, f"Order #{order.id} placed!")
    return redirect('orders:detail', order.id)


@login_required
def invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    payload = f"PAY://ORDER/{order.id}/AMT/{order.total_price:.2f}"
    qr_img = qrcode.make(payload)

    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'orders/invoice.html', {
        'order': order,
        'qr_code': qr_b64,
    })
