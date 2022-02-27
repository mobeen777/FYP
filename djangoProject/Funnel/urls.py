from django.urls import path
from .views import *

urlpatterns = [
    path('all_events/', GetAllEvents.as_view(), name='all_events'),
    path('event_count/', GetAllEventsCount.as_view(), name='event_count'),
    path('drop/', GetPercentageDrop.as_view(), name='drop'),
    path('total_drop/', GetPercentageDropTotal.as_view(), name='total_drop'),
    path('time/', GetAverageTime.as_view(), name='time'),
    path('event_filters/', GetEventsAndFilters.as_view(), name='event_filters'),
    path('filtered_count/', GetCountAfterFilter.as_view(), name='filtered_count'),

    # All Results on this url
    path('', GetAllResults.as_view(), name='event_count'),
]
