from django.contrib import admin
from .models import Machine, Metric, Incident
# Register your models here.
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'id']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['machine', 'cpu', 'memory', 'disk', 'uptime', 'timestamp']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['machine', 'incident_type', 'created_at', 'resolve_at', 'active']