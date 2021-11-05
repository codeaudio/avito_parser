from django.urls import path

from .view import redis_view

app_name = 'api'

urlpatterns = [
    path('v1/redis/', redis_view),
]
