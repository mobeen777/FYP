from Funnel.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from datetime import datetime


# Create your views here.

class GetAllEvents(APIView):
    """Send all Events in our Database"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = get_all_events()
        data = {
            'All_Events': data
        }
        return Response(data=data)


class GetFlowLayers(APIView):
    """Getting Flow layers of given event upto given number"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        no_of_layers = self.request.data[0]
        event = self.request.data[1]
        data_previous = previous_data(no_of_layers, event)
        data_next = next_data(no_of_layers, event)
        data = [data_previous, data_next]

        return Response(data=data)


def get_all_events():
    """Getting all events in our database"""

    all_events = Funnel.objects.all().values_list('event',
                                                  flat=True).distinct()
    return all_events


def getting_event_time_session():
    """Getting all unique Session IDs of Users/Events"""

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


"""Code for Previous/Backward Flow Layers"""


def previous_flow_of_events(event, events, sessions):
    """Getting previous events list"""

    layer = []
    for i in sessions:
        one_session = list(filter(lambda x: i in x, events))
        flow_event = list(filter(lambda x: event in x, one_session))

        for j in flow_event:
            time_value = 0
            goal_event = 0
            previous_event = []

            for k in one_session:
                if (k[1] < j[1]) and (k[1] > time_value):
                    time_value = k[1]
                    goal_event = k[0]
            if goal_event != event:
                previous_event.append(goal_event)
                layer.append(previous_event)

    return layer


def calc_no_of_events(layer):
    """Calculating no of events"""

    unique = []
    event_count = []
    for i in layer:
        if i not in unique and i != [0]:
            unique.append(i)

    for i in unique:
        count = 0
        for j in layer:
            if i == j:
                count += 1
        event_count.append((i[0], count))

    count_db = Funnel.objects.values('event').annotate(count=Count('event'))
    per_count = []
    for i in count_db:
        for j in event_count:
            if i['event'] == j[0]:
                per_count.append((j[0], (j[1] / i["count"]) * 100))
    return per_count


def previous_layer(target_event):
    """Getting previous layer of event"""

    session_id = getting_event_time_session()
    list_of_previous_event = previous_flow_of_events(target_event, session_id[0], session_id[1])
    previous_events = calc_no_of_events(list_of_previous_event)

    return previous_events


def all_previous_layers(total_layer, event):
    """Getting all previous layers of events"""

    all_events = []
    previous = previous_layer(event)

    if total_layer == 1:
        return previous
    else:
        for i in previous:
            previous_list = all_previous_layers(total_layer - 1, i[0])
            all_events.append({"Event": i[0],
                               "Percentage": i[1],
                               "Previous_Events": previous_list})
    return all_events


def previous_data(total, event):
    """Data which we will send"""
    data = [{"Layers": "Previous",
             "layer_no": 0,
             "Event": event}]
    for i in range(1, total + 1):
        data.append({"layer_no ": i,
                     "Events": all_previous_layers(i, event)})
    return data


"""Code for Forward/Next Flow Layers"""


def next_flow_of_events(event, events, sessions):
    """Getting list of Next events """

    next_layers = []
    for i in sessions:
        one_session = list(filter(lambda x: i in x, events))
        flow_event = list(filter(lambda x: event in x, one_session))

        for j in flow_event:
            time_value = 0
            goal_event = 0
            next_event = []
            count = 0
            for k in one_session:
                if count == 0:
                    if k[1] > j[1]:
                        time_value = k[1]
                        goal_event = k[0]
                        count += 1
                else:
                    if (k[1] > j[1]) and (k[1] <= time_value):
                        time_value = k[1]
                        goal_event = k[0]
            if goal_event != event:
                next_event.append(goal_event)
                next_layers.append(next_event)

    return next_layers


def next_layer(target_event):
    """Getting next layer of event"""

    session_id = getting_event_time_session()
    list_of_next_event = next_flow_of_events(target_event, session_id[0], session_id[1])
    next_events = calc_no_of_events(list_of_next_event)

    return next_events


def all_next_layers(total_layer, event):
    """Getting all next layers of events"""

    all_events = []
    next1 = next_layer(event)

    if total_layer == 1:
        return next1
    else:
        for i in next1:
            next_list = all_next_layers(total_layer - 1, i[0])
            all_events.append({"Event": i[0],
                               "Percentage": i[1],
                               "next_Events": next_list})
    return all_events


def next_data(total, event):
    """Data which we will send"""

    data = [{"Layers": "Next",
             "layer_no": 0,
             "Event": event}]
    for i in range(1, total + 1):
        data.append({"layer_no ": i,
                     "Events": all_next_layers(i, event)})
    return data
