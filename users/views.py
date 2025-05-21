from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from food.models import Category
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {"form": form})


@login_required
def profile(request):
    profile = request.user.profile
    regular = Category.objects.exclude(
        slug=f"{request.user.username}-choice"
    ).order_by('name')

    # Are we editing the favorite?
    editing = request.GET.get('edit_fav') == '1'

    if request.method == 'POST' and 'favorite' in request.POST:
        # Save the selected favorite
        cat = get_object_or_404(Category, id=request.POST['favorite'])
        profile.favorite = cat
        profile.save()
        messages.success(request, f"Favorite set to {cat.name}")
        return redirect('profile')

    return render(request, 'users/profile.html', {
        'editing_fav': editing,
        'regular_categories': regular,
    })
