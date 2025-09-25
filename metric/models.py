from django.db import models
import uuid
# Create your models here.


class Machine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    ip = models.URLField()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name
    


class Metric(models.Model):
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()
    disk = models.PositiveIntegerField()
    uptime = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='metrics')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.machine.name} | CPU: {self.cpu}% | {self.timestamp}"
    

class Incident(models.Model):
    TYPE_CHOICES = [
        ('CPU', 'CPU'),
        ('MEMORY', 'Memory'),
        ('DISK', 'Disk'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='incidents')
    incident_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_at =  models.DateTimeField(auto_now_add=True)
    resolve_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.incident_type} incident on {self.machine.name} ({'active' if self.active else 'resolved'})'