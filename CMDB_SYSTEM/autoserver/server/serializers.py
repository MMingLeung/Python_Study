#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
RestFrameWord组件的自定义序列化及验证
'''
from rest_framework import serializers
from repository import models

class MySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hostname = serializers.CharField(max_length=32)

    def validata_hostname(self, value):
        '''
        钩子
        :param value: 
        :return: 
        '''

        return value

    def update(self, instance, validated_data):
        instance.hostname = validated_data['hostname']
        instance.save()

    def create(self, validated_data):
        models.Asset.objects.create(**validated_data)