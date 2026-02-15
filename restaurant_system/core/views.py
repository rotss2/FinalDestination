from django.shortcuts import render
from menu.models import Category, MenuItem
from reservations.models import Reservation, Announcement

def home(request):
    # quick stats
    latest_announcements = Announcement.objects.order_by('-created_at')[:3]
    featured_items = MenuItem.objects.filter(is_available=True).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {
        'latest_announcements': latest_announcements,
        'featured_items': featured_items,
    })

def about(request):
    return render(request, 'core/about.html')
