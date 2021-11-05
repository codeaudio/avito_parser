from rest_framework.utils import json

from database.database_redis import Redis
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from config.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)._connect()


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def redis_view(request):
    return Response(json.loads(json.dumps(redis.get_all())), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def redis_detail_view(request, user_id):
    return Response(json.loads(json.dumps(redis.get(user_id))), status=status.HTTP_200_OK)
