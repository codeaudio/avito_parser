from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.utils import json

from config.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from database.database_redis import Redis
from utils.decorator import info_logger

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)._connect()


@info_logger
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def redis_view(request):
    if request.method == 'GET':
        return Response(json.loads(json.dumps(redis.get_all())), status=status.HTTP_200_OK)
    if request.method == 'POST':
        key = list(json.loads(request.body))
        if len(key) > 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            key = key[0]
            if not key in redis.get_keys():
                redis.save(key, dict(json.loads(request.body)).get(key))
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@info_logger
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAdminUser])
def redis_detail_view(request, user_id):
    if request.method in ('PUT', 'PATCH'):
        try:
            data = json.loads(request.body)
            redis.save(user_id, data)
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return Response(json.loads(json.dumps(redis.get(user_id))), status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        redis.delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
