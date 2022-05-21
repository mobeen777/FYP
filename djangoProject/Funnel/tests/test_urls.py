from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Funnel.views import *
from Flow import views
from AHAMoment.views import *


class TestUrls(SimpleTestCase):
    """Test cases to check if correct urls and relative ftns are being called"""

    def test_all_events_url_is_resolved(self):
        url = reverse('all_event')
        self.assertEqual(resolve(url).func.view_class, GetAllEvents)

    def test_event_count_url_is_resolved(self):
        url = reverse('event_counts')
        self.assertEqual(resolve(url).func.view_class, GetAllEventsCount)

    def test_drop_url_is_resolved(self):
        url = reverse('drop')
        self.assertEqual(resolve(url).func.view_class, GetPercentageDrop)

    def test_total_drop_url_is_resolved(self):
        url = reverse('total_drop')
        self.assertEqual(resolve(url).func.view_class, GetPercentageDropTotal)

    def test_time_url_is_resolved(self):
        url = reverse('time')
        self.assertEqual(resolve(url).func.view_class, GetAverageTime)

    def test_event_filters_url_is_resolved(self):
        url = reverse('event_filters')
        self.assertEqual(resolve(url).func.view_class, GetEventsAndFilters)

    def test_filtered_count_url_is_resolved(self):
        url = reverse('filtered_count')
        self.assertEqual(resolve(url).func.view_class, GetCountAfterFilter)

    def test_all_layers_url_is_resolved(self):
        url = reverse('layers')
        self.assertEqual(resolve(url).func.view_class, views.GetFlowLayers)

    def test_event_url_is_resolved(self):
        url = reverse('all_events')
        self.assertEqual(resolve(url).func.view_class, views.GetAllEvents)

    def test_correlation_url_is_resolved(self):
        url = reverse('correlation')
        self.assertEqual(resolve(url).func.view_class, GetCorrelation)

    def test_correlation_time_url_is_resolved(self):
        url = reverse('time_correlation')
        self.assertEqual(resolve(url).func.view_class, GetTimeCorrelation)
