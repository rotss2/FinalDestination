from django.shortcuts import render
from reservations.models import Announcement

def live_board(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:25]
    return render(request, "announcements/live_board.html", {"announcements": announcements})
