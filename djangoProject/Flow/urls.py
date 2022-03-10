from django.urls import path
from .views import *

urlpatterns = [
    path('layers/', GetFlowLayers.as_view(), name='layers'),
    path('all_events', GetAllEvents.as_view(), name='all_events'),
]
