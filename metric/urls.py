from django.urls import path
from .views import incidents_api, incidents_page

urlpatterns = [
    path('api/incidents/', incidents_api, name='incidents_api'),
    path('view/incident/', incidents_page, name='incidents_page')
]
