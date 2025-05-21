from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import ItemForm
from .models import Item, Category
from django.template import loader
from django.views.generic import ListView, TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse


class LandingPageView(TemplateView):
    template_name = 'food/landing.html'

class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'


def item(request):
    return HttpResponse("Hello, world. You're at item.")


class DetailClassView(DetailView):
    model = Item
    template_name = 'food/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        raw = (self.object.ingredients or "").strip()
        context['ingredients_list'] = [
            ing.strip() for ing in raw.split(',') if ing.strip()
        ]
        return context


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        # redirect to the detail page for this item
        return redirect('food:detail', item.id)
    return render(request, 'food/item_form.html', {'form': form, 'item': item})


class CreateItem(CreateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image', 'category', 'ingredients']
    template_name = 'food/item_form.html'

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get('category')
        if slug:
            cat = get_object_or_404(Category, slug=slug)
            initial['category'] = cat.pk
        return initial

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # after saving, self.object is the new Item
        return reverse('food:detail', args=[self.object.pk])


class CategoryView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        # look up the Category, 404 if not found
        self.category_obj = get_object_or_404(Category, slug=self.kwargs['category'])
        # return only items in that category
        return self.category_obj.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass the category name for the header
        context['category_name'] = self.category_obj.name
        return context

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item_delete.html', {'item': item})
