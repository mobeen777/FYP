# from django.test import RequestFactory
# from django.urls import reverse, resolve
# from Funnel.views import *
# import pytest
#
#
# class TestViews:
#     def test_all_events(self):
#         path = reverse('all_events')
#         request = RequestFactory().post(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_events_count(self):
#         path = reverse('event_count')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_drop(self):
#         path = reverse('drop')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_total_drop(self):
#         path = reverse('total_drop')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_time(self):
#         path = reverse('time')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_event_filters(self):
#         path = reverse('event_filters')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
#
#     def test_filtered_count(self):
#         path = reverse('filtered_count')
#         request = RequestFactory().get(path)
#
#         res = GetAllEvents.as_view()(request)
#
#         assert res.status_code == 200
