from django.test import TestCase, Client
from metric.models import Machine, Incident

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.machine = Machine.objects.create(name='TestMachine', ip='127.0.0.1')
        self.api_key = 'supersecretkey'

    def test_mock_metrics_view(self):
        response = self.client.get('/metric/mock-metrics/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('cpu', data)
        self.assertIn('memory', data)
        self.assertIn('disk', data)
        self.assertIn('uptime', data)

    def test_incident_api_auth(self):
        response = self.client.get('/metrics/api/incidents/')
        self.assertEqual(response.status_code, 401)
        response = self.client.get('/metrics/api/incidents/', HTTP_X_API_KEY=self.api_key)
        self.assertEqual(response.status_code, 200)

    def test_incident_api_data(self):
        Incident.objects.create(machine=self.machine, incident_type='CPU')
        response = self.client.get('metrics/api/incidents/', HTTP_X_API_KEY=self.api_key)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['machine'], self.machine.name)
        self.assertEqual(data[0]['type'], 'CPU')