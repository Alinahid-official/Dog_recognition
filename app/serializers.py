from dataclasses import field
from rest_framework import serializers
from .models import Dog

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields='__all__'