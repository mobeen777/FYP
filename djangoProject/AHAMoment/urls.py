from django.urls import path
from .views import *

urlpatterns = [
    path('correlation/', GetCorrelation.as_view(), name='correlation'),
    path('time_correlation/', GetTimeCorrelation.as_view(), name='time_correlation'),
]
