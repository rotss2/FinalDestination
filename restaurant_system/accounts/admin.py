from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Extra", {"fields": ("phone", "is_support")}),
    )
    list_display = ("username", "email", "is_staff", "is_support", "is_active")
    list_filter = ("is_staff", "is_support", "is_active")
