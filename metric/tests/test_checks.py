from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from metric.models import Machine, Metric, Incident
from metric.checks import check_cpu, check_disk, check_memory

class ChecksTests(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(name='TestMachine', ip='127.0.0.1')

    def test_check_cpu_creates_incident(self):
        Metric.objects.create(machine=self.machine, cpu=90, memory=50, disk=50, uptime='1h')
        check_cpu(self.machine)
        self.assertTrue(Incident.objects.filter(machine=self.machine, incident_type='CPU').exists())

    
    def test_check_memory_creates_incident(self):
        timestamp = timezone.now() - timedelta(minutes=30)
        Metric.objects.create(machine=self.machine, cpu=50, memory=95, disk=50, uptime='1h', timestamp=timestamp)
        check_memory(self.machine)
        self.assertTrue(Incident.objects.filter(machine=self.machine, incident_type='MEMORY').exists())

    def test_check_disk_creates_incident(self):
        timestamp =timezone.now() - timedelta(hours=1, minutes=30)
        Metric.objects.create(machine=self.machine, cpu=50, memory=50, disk=95, uptime='1h', timestamp=timestamp)
        check_disk(self.machine)
        self.assertTrue(Incident.objects.filter(machine=self.machine, incident_type='DISK').exists())

    def test_no_duplicate_active_incidents(self):
        Metric.objects.create(machine=self.machine, cpu=90, memory=50, disk=50, uptime='1h')
        check_cpu(self.machine)
        check_cpu(self.machine)
        self.assertEqual(Incident.objects.filter(machine=self.machine, incident_type='CPU').count(), 1)