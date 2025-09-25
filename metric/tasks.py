from celery import shared_task
from .models import Machine
from .utils import fetch_metrics
from .checks import check_cpu, check_disk, check_memory
import logging

logger = logging.getLogger(__name__)

@shared_task
def collect_metrics_task():
    for machine in Machine.objects.all():
        success = fetch_metrics(machine)
        if success: 
            logger.info(f"[OK] Metrics collected from {machine.name}")
            check_cpu(machine)
            check_memory(machine)
            check_disk(machine)
        else:
            logger.error(f"[FAIL] Could not fetch metrics from {machine.name}")