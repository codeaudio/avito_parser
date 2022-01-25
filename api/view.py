from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.serializers import (redisDetailSerializer, redisSerializer,
                             redisPostSerializer, redisDeleteSerializer,
                             redisPutPatchSerializer)
from config.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from database.database_redis import Redis
from utils.decorator import info_logger

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)._connect()


@info_logger
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def redis_view(request):
    if request.method == 'GET':
        serialize = redisSerializer(data=redis.get_all())
        serialize.is_valid(raise_exception=True)
        return Response(serialize.validated_data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serialize = redisPostSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.validated_data, status=status.HTTP_201_CREATED)


@info_logger
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAdminUser])
def redis_detail_view(request, user_id):
    if request.method == 'GET':
        serialize = redisDetailSerializer(
            data=redis.get(user_id), context={'user_id': user_id}
        )
        serialize.is_valid(raise_exception=True)
        return Response(serialize.validated_data, status=status.HTTP_200_OK)
    if request.method in ('PUT', 'PATCH'):
        serialize = redisPutPatchSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.update(user_id)
        return Response(serialize.validated_data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        redisDeleteSerializer().delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
