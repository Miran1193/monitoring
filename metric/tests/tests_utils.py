from django.test import TestCase
from unittest.mock import patch
from metric.models import Machine, Metric
from metric.utils import fetch_metrics

class UtilsTests(TestCase):
    def setUp(self):
        self.machine = Machine.object.create(name='TestMachine', ip='127.0.0.1')

    @patch('metric.utils.requests.get')
    def test_fetch_metrics_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'cpu': 50, 'memory': 30, 'disk': 40, 'uptime': '1d 1h'
        }

        result = fetch_metrics(self.machine)
        self.assertTrue(result)
        metric = Metric.objects.filter(machine=self.machine).first()
        self.assertIsNotNone(metric)
        self.assertEqual()
        self.assertEqual(metric.cpu, 50)
        self.assertEqual(metric.memory, 30)
        self.assertEqual(metric.disk, 40)

    @patch('metrics.utils.requests.get')
    def test_fetch_metrics_failure(self, mock_get):
        mock_get.side_effect = Exception('Network error')
        result = fetch_metrics(self.machine)
        self.assertFalse(result)

