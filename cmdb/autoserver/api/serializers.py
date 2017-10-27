from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from repository import models
from repository import models


class MySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    email = serializers.CharField()

    def validate_name(self, value):
        pass

    def validate_email(self, value):
        #钩子
        return value


    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.email = validated_data['email']
        instance.save()


    def create(self, validated_data):
        # models.xx.xx
        models.UserProfile.objects.create(**validated_data)
