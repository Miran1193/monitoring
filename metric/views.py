from django.shortcuts import render
from django.http import JsonResponse
import random, requests
import logging
from .models import Incident
# Create your views here.



logger = logging.getLogger(__name__)

def mock_metrics(request):
    return JsonResponse({
        'cpu': random.randint(10, 100),
        'memory': f"{random.randint(10, 100)}%",
        'disk': f"{random.randint(10, 100)}%",
        'uptime': '1d 23h 35m'
    })


def incidents_api(request):
    incidents = Incident.objects.filter(active=True).order_by('-created_at')
    data = [
        {
            'id': inc.id,
            'machine': inc.machine.name,
            'type': inc.incident_type,
            'created': inc.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for inc in incidents
    ]
    return JsonResponse(data, safe=False)

def incidents_page(request):
    return render(request, 'incidents.html')
    



