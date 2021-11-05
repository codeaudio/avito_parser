from django.urls import path

from .view import redis_view, redis_detail_view

app_name = 'api'

urlpatterns = [
    path('v1/redis/', redis_view),
    path('v1/redis/<str:user_id>/', redis_detail_view),
]
