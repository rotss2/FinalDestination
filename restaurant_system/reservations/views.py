from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Reservation, Table, WalkInQueue
from .forms import ReservationForm
from .services import find_available_tables, refresh_queue_estimates

def staff_required(user):
    return user.is_authenticated and user.is_staff

@login_required
def portal(request):
    my_reservations = Reservation.objects.filter(user=request.user).order_by("-start_dt")
    return render(request, "reservations/portal.html", {"my_reservations": my_reservations})

@login_required
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_dt = form.cleaned_data["start_dt"]
            duration = form.cleaned_data["duration_minutes"]
            guests = form.cleaned_data["guests"]
            available = find_available_tables(start_dt, duration, guests)
            if not available.exists():
                messages.error(request, "No tables available for that time. Try another slot.")
            else:
                table = available.first()
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.table = table
                reservation.status = "confirmed"
                reservation.save()

                # Email notification (console by default)
                if request.user.email:
                    send_mail(
                        subject="Reservation Confirmed",
                        message=f"Your reservation is confirmed for {reservation.start_dt:%Y-%m-%d %H:%M} at Table {table.number}.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )

                messages.success(request, f"Reservation confirmed! Table {table.number} is reserved for you.")
                return redirect("reservations:portal")
    else:
        form = ReservationForm()
    return render(request, "reservations/create_reservation.html", {"form": form})

@login_required
def edit_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id, user=request.user)
    if reservation.status in ["cancelled", "completed"]:
        return HttpResponseForbidden("Cannot edit this reservation.")
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            start_dt = form.cleaned_data["start_dt"]
            duration = form.cleaned_data["duration_minutes"]
            guests = form.cleaned_data["guests"]

            # Temporarily exclude this reservation from conflict check
            others = Reservation.objects.exclude(id=reservation.id)
            available = find_available_tables(start_dt, duration, guests).exclude(id=reservation.table_id)
            # allow keeping same table if still fits and not overlapping
            # For simplicity: if any available tables, reassign; else keep if possible
            if not find_available_tables(start_dt, duration, guests).exists():
                messages.error(request, "No tables available for that time. Try another slot.")
            else:
                new_table = find_available_tables(start_dt, duration, guests).first()
                reservation = form.save(commit=False)
                reservation.table = new_table
                reservation.status = "confirmed"
                reservation.save()
                messages.success(request, "Reservation updated.")
                return redirect("reservations:portal")
    else:
        # prefill datetime-local value
        initial = {"start_dt": reservation.start_dt.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")}
        form = ReservationForm(instance=reservation, initial=initial)
    return render(request, "reservations/edit_reservation.html", {"form": form, "reservation": reservation})

@login_required
def cancel_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id, user=request.user)
    if request.method == "POST":
        reservation.status = "cancelled"
        reservation.save(update_fields=["status"])
        messages.success(request, "Reservation cancelled.")
        return redirect("reservations:portal")
    return render(request, "reservations/cancel_reservation.html", {"reservation": reservation})

def check_availability(request):
    # AJAX endpoint: ?start_dt=YYYY-MM-DDTHH:MM&duration=90&guests=2
    try:
        start_dt = request.GET.get("start_dt")
        duration = int(request.GET.get("duration", "90"))
        guests = int(request.GET.get("guests", "2"))
        if not start_dt:
            raise ValueError("missing start_dt")
        dt = timezone.datetime.fromisoformat(start_dt)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        tables = find_available_tables(dt, duration, guests)
        return JsonResponse({
            "ok": True,
            "available_count": tables.count(),
            "suggested_table": tables.first().number if tables.exists() else None,
        })
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

# Walk-in queue (staff)
@user_passes_test(staff_required)
def queue_board(request):
    refresh_queue_estimates()
    queue = WalkInQueue.objects.all()
    return render(request, "reservations/queue_board.html", {"queue": queue})

@user_passes_test(staff_required)
def add_walkin(request):
    if request.method == "POST":
        party_size = int(request.POST.get("party_size", "2"))
        w = WalkInQueue.objects.create(party_size=party_size)
        refresh_queue_estimates()
        messages.success(request, f"Added walk-in party of {party_size}.")
    return redirect("reservations:queue_board")
