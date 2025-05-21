from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_combo_to_cart/<int:combo_id>/', views.add_combo_to_cart, name='add_combo_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    # after placing, show the real Order + its items
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/invoice/', views.invoice, name='invoice'),
]
