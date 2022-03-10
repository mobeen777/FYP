from django.urls import path
from .views import *

urlpatterns = [
    path('layers/', GetFlowLayers.as_view(), name='all_events'), ]
