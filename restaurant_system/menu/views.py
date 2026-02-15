from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem

def menu_home(request):
    categories = Category.objects.all()
    return render(request, "menu/menu_home.html", {"categories": categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.items.filter(is_available=True)
    return render(request, "menu/category_detail.html", {"category": category, "items": items})

def item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return render(request, "menu/item_detail.html", {"item": item})
