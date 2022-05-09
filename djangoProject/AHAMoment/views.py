from Funnel.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from datetime import datetime


def get_all_events():
    """Getting all events in our database"""

    all_events = Funnel.objects.all().values_list('event',
                                                  flat=True).distinct()
    return all_events
