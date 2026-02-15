from django.contrib import admin
from .models import Table, Reservation, WalkInQueue, Announcement

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "capacity", "table_type", "is_active")
    list_filter = ("table_type", "is_active")
    search_fields = ("number",)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "table", "start_dt", "guests", "status")
    list_filter = ("status", "table__table_type")
    search_fields = ("user__username", "table__number")
    date_hierarchy = "start_dt"

@admin.register(WalkInQueue)
class WalkInQueueAdmin(admin.ModelAdmin):
    list_display = ("arrival_dt", "party_size", "status", "estimated_wait_minutes")
    list_filter = ("status",)
    date_hierarchy = "arrival_dt"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "is_active", "created_at")
    list_filter = ("priority", "is_active")
    search_fields = ("title",)
