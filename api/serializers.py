from rest_framework import serializers, status

from rest_framework.serializers import Serializer

from api.exceptions import CustomApiException
from config.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from database.database_redis import Redis

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)._connect()


class redisDetailSerializer(Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    search_object = serializers.CharField()
    city = serializers.CharField(allow_blank=True)
    min_price = serializers.CharField(allow_blank=True)
    max_price = serializers.CharField(allow_blank=True)
    max_object = serializers.CharField(allow_blank=True)

    def validate_empty_values(self, data):
        if self.context['user_id'] not in redis.get_keys():
            raise CustomApiException(
                detail={f"key {self.context['user_id']} Not Found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return super().validate_empty_values(data)


class redisSerializer(Serializer):

    def validate(self, *args, **kwargs):
        fields = [
            'username', 'last_name', 'first_name',
            'search_object', 'city', 'min_price', 'max_price', 'max_object'
        ]
        for key in self.initial_data:
            diff = set(fields).symmetric_difference(self.initial_data[key].keys())
            if diff:
                raise serializers.ValidationError(
                    detail={'expected fields': diff}
                )
        return self.initial_data

    def to_representation(self, data):
        return self.initial_data


class redisPostSerializer(Serializer):

    def validate(self, *args, **kwargs):
        json_obj = self.initial_data
        key = list(json_obj)
        if len(key) > 1:
            raise serializers.ValidationError(
                detail='too many keys'
            )
        return self.initial_data

    def save(self, **kwargs):
        key = list(self.initial_data)
        if len(key) > 1:
            return
        key = key[0]
        if key not in redis.get_keys():
            redis.save(key, dict(self.initial_data).get(key))
        else:
            raise serializers.ValidationError(
                detail='key exists'
            )
        return self.initial_data

    def to_representation(self, data):
        return self.initial_data


class redisPutPatchSerializer(Serializer):
    def validate(self, *args, **kwargs):
        fields = [
            'username', 'last_name', 'first_name',
            'search_object', 'city', 'min_price', 'max_price', 'max_object'
        ]
        diff = set(fields).symmetric_difference(self.initial_data.keys())
        if diff:
            raise serializers.ValidationError(
                detail={'expected fields': diff}
            )
        if self.initial_data.get('username') == '':
            raise serializers.ValidationError(
                detail='username can not be blank'
            )
        return self.initial_data

    def update(self, user_id=None, **kwargs):
        if user_id in redis.get_keys():
            redis.save(user_id, self.initial_data)
        else:
            raise serializers.ValidationError(
                detail='key exists'
            )
        return self.initial_data

    def to_representation(self, data):
        return self.initial_data


class redisDeleteSerializer(Serializer):

    def validate(self, *args, **kwargs):
        key = list(self.initial_data)
        if key not in redis.get_keys():
            raise serializers.ValidationError(
                detail='key has been deleted'
            )
        return self.initial_data

    def delete(self, user_id):
        if user_id not in redis.get_keys():
            raise serializers.ValidationError(
                detail='key has been deleted'
            )
        redis.delete(user_id)
