import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import base64
import io
from food.models import CustomCombo, Item
from orders.models import Order, OrderItem


# Create your views here.

@login_required
def add_item_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # 1) create a brand‐new Order
    order = Order.objects.create(user=request.user)
    # 2) add exactly 1 of that item
    OrderItem.objects.create(order=order, item=item, quantity=1)
    return redirect('orders:detail', order.id)

@login_required
def add_combo_order(request, combo_id):
    combo = get_object_or_404(CustomCombo, pk=combo_id, user=request.user)
    order = Order.objects.create(user=request.user)
    for item in combo.items.all():
        OrderItem.objects.create(order=order, item=item, quantity=1)
    return redirect('orders:detail', order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def invoice(request, order_id):
    # 1) Load the order, ensure it belongs to this user
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    # 2) Build a dummy “PAY://” QR payload
    payload = f"PAY://ORDER/{order.id}/AMT/{order.total_price:.2f}"
    qr_img  = qrcode.make(payload)

    # 3) Encode to base64 so we can inline it in HTML
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    # 4) Render the invoice template
    return render(request, 'orders/invoice.html', {
        'order':    order,
        'qr_code':  qr_b64,
    })