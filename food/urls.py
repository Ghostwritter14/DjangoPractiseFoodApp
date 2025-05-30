from . import views
from django.urls import path

from .views import LandingPageView

app_name = 'food'
urlpatterns = [
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('menu', views.IndexClassView.as_view(), name='menu'),

    path('<int:pk>/', views.DetailClassView.as_view(), name='detail'),
    path('item/', views.item, name='item'),

    path('add/', views.CreateItem.as_view(), name='create_item'),

    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('', views.IndexClassView.as_view(), name='index'),

    path('update/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]

