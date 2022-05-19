from Funnel.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import math
from django.db.models import Count
from datetime import datetime


class GetCorrelation(APIView):
    """Sending Phi Correlation"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        event = self.request.data["data"]
        event = event["event"]
        data = phi_correlation(event)
        print("no")
        data = {
            'All_Events': data
        }
        return Response(data=data)


class GetTimeCorrelation(APIView):
    """Sending Phi Correlation on Time Series"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        events = self.request.data["data"]
        event = events["event"]
        time = events["time"]
        data = phi_correlation_time(event, time)
        print("yes")
        data = {
            'All_Events': data
        }
        return Response(data=data)


def get_all_events():
    """Getting all events in our database"""

    all_events = Funnel.objects.all().values_list('event',
                                                  flat=True).distinct()
    events = []
    for i in all_events:
        events.append(i)
    return all_events


def unique_ids():
    """Getting Events with session IDs"""

    obj1 = Funnel.objects.all().values()

    all_events = []
    unique_ids_list = []

    # creating list of tuple [(event,time,session_id)]

    for i in obj1:
        datetime_object = datetime.strptime(i["properties"][0]["timestamp"], "%m-%d-%Y %H:%M:%S")
        time = datetime_object.timestamp()
        all_events.append((i["event"], time, i["properties"][0]["session_id"]))

        if i["properties"][0]["session_id"] not in unique_ids_list:
            unique_ids_list.append(i["properties"][0]["session_id"])

    return all_events, unique_ids_list


def phi_correlation(event):
    """Performing phi correlation"""

    data = unique_ids()
    events = get_all_events()

    for i in data[1]:
        one_session = list(filter(lambda x: i in x, data[0]))
    all_correlation = []
    for i in events:
        a = 1
        b = 1
        c = 1
        d = 1
        for j in data[1]:
            n1 = 0
            n0 = 0
            for k in data[0]:

                if i == k[0] and j == k[2]:
                    n1 = 1

                if event == k[0] and j == k[2]:
                    n0 = 1

            if n1 == 1 and n0 == 1:
                a += 1
            if n1 == 1 and n0 == 0:
                b += 1
            if n1 == 0 and n0 == 1:
                c += 1
            if n1 == 0 and n0 == 0:
                d += 1
        ad = a * d
        bc = b * c
        print(a, b, c, d)
        e = ad - bc
        under = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
        correlation = e / under
        all_correlation.append([event, i, correlation])

    return all_correlation


def unique_user_ids():
    """Getting Events with User IDs"""

    obj1 = Funnel.objects.all().values()

    all_events = []
    unique_user_ids_list = []

    # creating list of tuple [(event,time,session_id)]

    for i in obj1:
        datetime_object = datetime.strptime(i["properties"][0]["timestamp"], "%m-%d-%Y %H:%M:%S")
        time = datetime_object.timestamp()
        all_events.append((i["event"], time, i["properties"][0]["user_id"]))

        if i["properties"][0]["user_id"] not in unique_user_ids_list:
            unique_user_ids_list.append(i["properties"][0]["user_id"])

    return all_events, unique_user_ids_list


def first_event(all_events, unique_user_ids_list):
    """Finding first event by the user"""

    event = all_events[1]
    first = event[1]
    all_first_events = []
    for i in unique_user_ids_list:
        for j in all_events:

            if i == j[2] and first > j[1]:
                first = j[1]
        all_first_events.append({"user_id": i,
                                 "time": first})
    # print(all_first_events)
    return all_first_events


def phi_correlation_time(event, time):
    """Performing Phi Correlation on Time Series"""

    data = unique_user_ids()
    events = get_all_events()

    event_first = first_event(data[0], data[1])

    for i in data[1]:
        one_session = list(filter(lambda x: i in x, data[0]))
    all_correlation = []
    for i in events:
        a = 1
        b = 1
        c = 1
        d = 1
        for l in event_first:
            n1 = 0
            n0 = 0
            for k in data[0]:

                if i == k[0] and l["user_id"] == k[2] and (l["time"] + (time * 604000)) >= k[1]:
                    n1 = 1
                if event == k[0] and l["user_id"] == k[2] and (l["time"] + (time * 604000)) >= k[1]:
                    n0 = 1
            if n1 == 1 and n0 == 1:
                a += 1
            if n1 == 1 and n0 == 0:
                b += 1
            if n1 == 0 and n0 == 1:
                c += 1
            if n1 == 0 and n0 == 0:
                d += 1
        ad = a * d
        bc = b * c
        print(a, b, c, d)
        e = ad - bc
        under = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
        correlation = e / under
        all_correlation.append([event, i, correlation])

    return all_correlation
