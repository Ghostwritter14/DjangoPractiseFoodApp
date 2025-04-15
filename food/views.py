from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import models
from .forms import ItemForm
from .models import Item
from django.template import loader
from django.views.generic import ListView
from django.views.generic import DetailView


# Create your views here.
# def index(request):
#     item_list = Item.objects.all()
#     #template = loader.get_template('food/index.html')
#     context = {
#         'item_list': item_list,
#     }
#     return render(request, 'food/index.html', context)

class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'


def item(request):
    return HttpResponse("Hello, world. You're at item.")


# def detail(request, item_id):
#     item = Item.objects.get(pk=item_id)
#     context = {
#         'item': item
#     }
#     return render(request, 'food/detail.html', context)


class DetailClassView(DetailView):
    model = Item
    template_name = 'food/detail.html'


def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request, 'food/item_form.html', {'form': form})


def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('food:index', item_id)
    return render(request, 'food/item_form.html', {'form': form, 'item': item})


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item_delete.html', {'item': item})
