from django.urls import path
from .views import *


urlpatterns = [
    path('session/', GetSession.as_view(), name='all_events'),]