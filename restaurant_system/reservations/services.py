from django.db.models import Q
from django.utils import timezone
from .models import Table, Reservation, WalkInQueue

def find_available_tables(start_dt, duration_minutes, guests, table_type=None):
    end_dt = start_dt + timezone.timedelta(minutes=duration_minutes)

    tables = Table.objects.filter(is_active=True, capacity__gte=guests)
    if table_type:
        tables = tables.filter(table_type=table_type)

    overlapping = Reservation.objects.filter(
        status__in=["pending","confirmed","seated"],
    ).filter(
        Q(start_dt__lt=end_dt) & Q(start_dt__gte=start_dt - timezone.timedelta(minutes=duration_minutes))
    )

    # More accurate overlap: any reservation whose time window overlaps [start,end)
    overlapping = Reservation.objects.filter(status__in=["pending","confirmed","seated"]).filter(
        Q(start_dt__lt=end_dt) & Q(start_dt__gte=start_dt - timezone.timedelta(minutes=duration_minutes))
    )
    # We'll compute overlap in python for simplicity:
    reserved_table_ids = set()
    for r in Reservation.objects.filter(status__in=["pending","confirmed","seated"]):
        r_end = r.end_dt
        if (r.start_dt < end_dt) and (r_end > start_dt):
            reserved_table_ids.add(r.table_id)

    return tables.exclude(id__in=reserved_table_ids).order_by("capacity", "number")

def estimate_wait_time_minutes(party_size):
    # Simple heuristic: based on active tables and current reservations.
    # Can be improved with queuing theory models (see project notes).
    now = timezone.now()
    open_tables = find_available_tables(now, 60, party_size)
    if open_tables.exists():
        return 0

    upcoming = []
    for r in Reservation.objects.filter(status__in=["pending","confirmed","seated"], start_dt__gte=now).order_by("start_dt")[:50]:
        if r.table.capacity >= party_size:
            upcoming.append(r.end_dt)
    if not upcoming:
        return 30
    soonest = min(upcoming)
    return max(5, int((soonest - now).total_seconds() // 60))

def refresh_queue_estimates():
    for w in WalkInQueue.objects.filter(status="waiting"):
        w.estimated_wait_minutes = estimate_wait_time_minutes(w.party_size)
        w.save(update_fields=["estimated_wait_minutes"])
