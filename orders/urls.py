from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add_item/<int:item_id>/', views.add_item_order, name='add_item'),
    path('add_combo/<int:combo_id>/', views.add_combo_order, name='add_combo'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/invoice/', views.invoice, name='invoice'),
]
