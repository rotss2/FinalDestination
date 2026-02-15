from django import forms
from django.utils import timezone
from .models import Reservation

class ReservationForm(forms.ModelForm):
    start_dt = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        help_text="Choose date and time."
    )

    class Meta:
        model = Reservation
        fields = ("start_dt", "duration_minutes", "guests", "notes")

    def clean_start_dt(self):
        dt = self.cleaned_data["start_dt"]
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        if dt < timezone.now():
            raise forms.ValidationError("Start time must be in the future.")
        return dt
