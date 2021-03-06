from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from datetime import datetime

# Create your views here.
"""Filter which used as Dummy"""

#
# input_filter = ["event": "cart",
#                  "filters": {
#                      "os_type": "Android 7.1.2",
#                  }
#                  }, {"event": "register",
#                      "filters": {
#                          "os_type": "Android 4.4",
#
#                      }
#                      },
#                 {'event': "payment_info",
#                  "filters": {
#                      "theme_color": "Red",
#                  }
#                  }
#                 ]


class GetAllEvents(APIView):
    """Send all Events in our Database"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_events = get_all_events()

        data = event_count(input_events)  # Passing funnel which we get from frontend
        data = {
            'All_Events': data
        }
        return Response(data=data)


class GetAllEventsCount(APIView):
    """Sending count of all events"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        input_events = self.request.data["data"]
        data = event_count(input_events)  # Passing funnel which we get from frontend
        all_events = []
        for i in input_events:
            for j in data:
                if i == j["event"]:
                    all_events.append(j)
        data = {
            'All_Events': all_events
        }
        return Response(data=data)


class GetPercentageDrop(APIView):
    """Sending Drop off"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_events = self.request.data["data"]
        count = event_count(input_events)  # Passing funnel which we get from frontend
        all_events = []
        for i in input_events:
            for j in count:
                if i == j["event"]:
                    all_events.append(j)
        drop = per_drop(all_events)

        data = {
            'Drop_Percentage': drop,
        }

        return Response(data=data)


class GetPercentageDropTotal(APIView):
    """Sending Drop off from total"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_events = self.request.data["data"]
        count = event_count(input_events)  # Passing funnel which we get from frontend
        all_events = []
        for i in input_events:
            for j in count:
                if i == j["event"]:
                    all_events.append(j)

        total_drop = total_per_drop(all_events)
        data = {
            'Total_Drop': total_drop
        }
        return Response(data=data)


class GetAverageTime(APIView):
    """Sending Average Time Taken"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_events = self.request.data["data"]
        time_avg = all_time(input_events)  # Passing funnel which we get from frontend
        print(time_avg)
        data = {
            'Average_Time': time_avg,
        }
        return Response(data=data)


class GetEventsAndFilters(APIView):
    """Sending All Events and Filters(Properties)"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        events = get_all_events()
        event_filter = all_events_filters(events)
        data = {
            'Event_Filter': event_filter,
        }
        return Response(data=data)


class GetCountAfterFilter(APIView):
    """Sending Event Counts of Relative Event After Applying the Filters"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_filter = self.request.data["data"]
        filtered_events = filter_for_all_events(input_filter)  # Filter define above later it will come from frontend
        data = {
            'Filtered_Events_Count': filtered_events,
        }
        return Response(data=data)


class GetAllResults(APIView):
    """Sending all analytics"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        input_filter = self.request.data[0]
        input_events = self.request.data[1]
        events = get_all_events()
        count = event_count(input_events)  # Passing funnel which we get from frontend
        drop = per_drop(count)
        total_drop = total_per_drop(count)
        time_avg = all_time(input_events)
        filtered_events = filter_for_all_events(input_filter)  # Filter define above later it will come from frontend
        event_filter = all_events_filters(events)
        data = {
            'All_Events': events,
            "Count": count,
            'Drop_Percentage': drop,
            'Total_Drop': total_drop,
            'Average_Time': time_avg,
            'Filtered_Events_Count': filtered_events,
            'Event_Filter': event_filter,
        }
        return Response(data=data)


"""Functions of Analytics"""


def get_all_events():
    """Getting all events in our database"""

    all_events = Funnel.objects.all().values_list('event',
                                                  flat=True).distinct()
    return all_events


def event_count(funnel):
    """Getting  events_count for distinct values in our database"""

    count = Funnel.objects.values('event').annotate(count=Count('event'))
    count_event = []
    for i in count:
        for j in funnel:
            if i['event'] == j:
                count_event.append(i)
    return count_event


def per_drop(count):
    """Getting drop off  event in the funnel"""

    drop_percentage = []
    for i in range(len(count)):
        if i == len(count) - 1:
            break
        print(count[i], count[i + 1])
        drop_percentage.append({"Event": f"{count[i]['event']}-{count[i + 1]['event']}",
                                "Drop": ((count[i]['count'] - count[i + 1]['count']) /
                                         count[i]['count']) * 100})

    return drop_percentage


def total_per_drop(count):
    """Getting drop off total event in the funnel"""

    total = 0
    for i in count:
        total += i['count']

    total_drop = []
    for i in range(len(count)):
        if i == len(count):
            break
        total_drop.append({"Event": f"Total-{count[i]['event']}",
                           "Total-Drop": ((total - count[i]['count']) /
                                          total) * 100}
                          )

    return total_drop


def timestamp(event):
    """Getting Average TimeStamps of Each Event"""

    time_stamp = Funnel.objects.values()

    total_time = 0
    count = 1

    for i in time_stamp:
        if i['event'] == event:
            for j in i['properties']:
                datetime_object = datetime.strptime(j['timestamp'], "%m-%d-%Y %H:%M:%S")
                total_time += datetime_object.timestamp()
            count += 1
    time_avg = (total_time / count)
    print(time_avg)
    return time_avg


def all_time(funnel):
    """Getting The Time Taken"""

    all_avg = []
    for i in range(len(funnel)):
        if i == len(funnel) - 1:
            break
        first_event = timestamp(funnel[i])
        second_event = timestamp(funnel[i + 1])
        avg = (first_event - second_event) / 60
        all_avg.append(avg)

    time_per_event = []
    for i in range(len(funnel)):
        if i == len(funnel) - 1:
            break
        time_per_event.append({"Event": f"{funnel[i]}-{funnel[i + 1]}",
                               "Time": all_avg[i]})

    return time_per_event


def event_and_filter(event):
    """Getting event and relative filter"""

    obj = Funnel.objects.filter(event=event).values()
    count = 0
    values = {}

    for i in obj[1]['properties'][0].keys():
        total = []
        for j in obj:
            if j['properties'][0][i] in total:
                pass
            else:
                total.append(j['properties'][0][i])
        a = list(obj[1]['properties'][0])
        if a[count] == 'timestamp' or a[count] == 'session_id':
            pass
        else:
            values[a[count]] = total
        count += 1

    event_filter = {
        event: values
    }
    return event_filter


def all_events_filters(event):
    """Getting events and relative filters(Properties mention in Json) for all"""

    events_filter = []
    for i in event:
        data = event_and_filter(i)
        events_filter.append(data)
    return events_filter


def filter_for_event(to_be_filter):
    """Function to apply filter"""

    obj = Funnel.objects.filter(properties__contains=to_be_filter['filters']).filter(
        event=to_be_filter['event']).count()
    after_filter = {
        'event': to_be_filter['event'],
        'count': obj,
    }
    return after_filter


def filter_for_all_events(filters):
    """Apply Filter Function on all the Event Which We Get From the frontend"""

    all_filtered_events = []
    print(len(filters))
    for i in range(len(filters)):
        obj = filter_for_event(filters[i])
        all_filtered_events.append(obj)
    return all_filtered_events
