from database.database_redis import Redis
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from config.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)._connect()


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def redis_view(*args):
    return Response(redis.get_all(), status=status.HTTP_200_OK)
