from rest_framework import serializers
from .models import UserLogin

class UserLoginserializer(serializers.ModelSerializer):

    class Meta:
        model = UserLogin
        fields = "__all__"