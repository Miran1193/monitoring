import os
import requests
from .models import Machine, Metric
import logging

logger = logging.getLogger(__name__)


def get_machine_data(url: str):
    try:
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к url: {e}")
        return None

def fetch_metrics(machine: Machine):

    use_mock = os.getenv('USE_MOCK_METRICS', 'False') == True
    if use_mock:
        url = 'http://localhost:8000/metric/mock_metrics/'
    else:
        url = f"http://{machine.ip}/metrics"

    data = get_machine_data(url)
    if not data:
        return False

    try:
        Metric.objects.create(
            machine=machine,
            cpu=float((data.get('cpu') or '0').strip('%')),
            memory=float((data.get('memory')or '0').strip('%')),
            disk=float((data.get('disk') or '0').strip('%')),
            uptime=data.get('uptime'),
        )
        return True
    
    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error(f"[ERROR] Failed to fetch metrics from {machine.name}: {e}")
        return False