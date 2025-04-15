from . import views
from django.urls import path
app_name = 'food'
urlpatterns = [
    path('', views.IndexClassView.as_view(), name='index'),
    # food
    path('<int:pk>/', views.DetailClassView.as_view(), name='detail'),
    path('item/', views.item, name='item'),
    # add items
    path('add', views.create_item, name='create_item'),
    #edit
    path('update/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),

]

