from Funnel.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from datetime import datetime


# Create your views here.

class GetSession(APIView):

    def get(self, request, *args, **kwargs):
        previous_events = previous_layer("search")
        # data = {
        #     "Target_Event": "search",
        #     "previous_layers": previous_events,
        # }
        data = my_code(3, previous_events)
        return Response(data=data)


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


def flow_of_events(event, events, sessions):
    """Getting list of previous events"""

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
    """Getting all layers of events"""

    session_id = getting_event_time_session()
    list_of_previous_event = flow_of_events(target_event, session_id[0], session_id[1])
    previous_events = calc_no_of_events(list_of_previous_event)

    return previous_events

