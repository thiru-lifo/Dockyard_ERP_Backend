from rest_framework import serializers
from .models import User
from access.serializer import Processserializer


class Userserializer(serializers.ModelSerializer):
    process = Processserializer(read_only=True)
    class Meta:
        model = User
        fields = "__all__"