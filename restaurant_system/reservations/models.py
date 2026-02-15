from django.db import models
from django.conf import settings
from django.utils import timezone

class Table(models.Model):
    TABLE_TYPES = (("indoor", "Indoor"), ("outdoor", "Outdoor"))
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    table_type = models.CharField(max_length=10, choices=TABLE_TYPES, default="indoor")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number} ({self.capacity})"

class Reservation(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("seated", "Seated"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="reservations")
    start_dt = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=90)
    guests = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_dt']

    @property
    def end_dt(self):
        return self.start_dt + timezone.timedelta(minutes=self.duration_minutes)

    def __str__(self):
        return f"{self.user} - {self.start_dt} - {self.table}"

class WalkInQueue(models.Model):
    STATUS = (("waiting","Waiting"),("seated","Seated"),("cancelled","Cancelled"))
    arrival_dt = models.DateTimeField(default=timezone.now)
    party_size = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=STATUS, default="waiting")
    estimated_wait_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['arrival_dt']

    def __str__(self):
        return f"Walk-in {self.party_size} @ {self.arrival_dt:%Y-%m-%d %H:%M}"

class Announcement(models.Model):
    title = models.CharField(max_length=140)
    message = models.TextField()
    priority = models.IntegerField(default=1, help_text="1=normal, 2=important, 3=urgent")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
