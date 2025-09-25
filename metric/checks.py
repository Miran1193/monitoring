from django.utils import timezone
from datetime import timedelta
from .models import Incident, Metric


def check_threshold(machine, field_name, threshold, period_minutes, incident_type):
    time_ago = timezone.now() - timedelta(minutes=period_minutes)
    metrics = machine.metrics.filter(timestamp__gte=time_ago)

    if metrics.filter(**{f"{field_name}__gt": threshold}).exists():
        create_incident(machine, incident_type)


def create_incident(machine, incident_type):
    active_exists = Incident.objects.filter(machine=machine, incident_type=incident_type, active=True).exists()

    if not active_exists:
        Incident.objects.create(machine=machine, incident_type=incident_type)


def check_cpu(machine):
    check_threshold(machine, 'cpu', 85, 5, 'CPU')

def check_memory(machine):
    check_threshold(machine, 'memory', 90, 30, 'MEMORY')

def check_disk(machine):
    check_threshold(machine, 'disk', 95, 120, 'DISK')