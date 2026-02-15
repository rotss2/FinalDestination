from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Avg
from reservations.models import Reservation, WalkInQueue, Table

def staff_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff_required)
def admin_dashboard(request):
    now = timezone.now()
    last_30 = now - timezone.timedelta(days=30)

    total_tables = Table.objects.filter(is_active=True).count()
    total_reservations = Reservation.objects.filter(created_at__gte=last_30).count()

    # Peak hours (by hour of day)
    hourly = (Reservation.objects.filter(start_dt__gte=last_30, status__in=["confirmed","seated","completed"])
              .extra(select={'hour': "strftime('%%H', start_dt)"})
              .values('hour')
              .annotate(count=Count('id'))
              .order_by('hour'))

    hours = [h['hour'] for h in hourly]
    counts = [h['count'] for h in hourly]

    # Occupancy rate (simple): reserved table slots today / tables
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)
    todays = Reservation.objects.filter(start_dt__gte=today_start, start_dt__lt=today_end, status__in=["confirmed","seated","completed"]).count()
    occupancy = 0 if total_tables == 0 else round((todays / total_tables) * 100, 1)

    avg_wait = WalkInQueue.objects.filter(arrival_dt__gte=last_30).aggregate(avg=Avg('estimated_wait_minutes'))['avg']
    avg_wait = round(avg_wait or 0, 1)

    return render(request, "dashboard/admin_dashboard.html", {
        "total_tables": total_tables,
        "total_reservations": total_reservations,
        "occupancy": occupancy,
        "avg_wait": avg_wait,
        "hours": hours,
        "counts": counts,
    })
