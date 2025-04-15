from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import models
from .forms import ItemForm
from .models import Item
from django.template import loader
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'


def item(request):
    return HttpResponse("Hello, world. You're at item.")


class DetailClassView(DetailView):
    model = Item
    template_name = 'food/detail.html'


def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('food:index', item_id)
    return render(request, 'food/item_form.html', {'form': form, 'item': item})


class CreateItem(CreateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image']
    template_name = 'food/item_form.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item_delete.html', {'item': item})
