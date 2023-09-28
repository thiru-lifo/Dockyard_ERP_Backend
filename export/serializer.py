
from rest_framework import serializers
from .models import IPL

#from django.contrib.auth import get_user_model # add this

#User = get_user_model()


class IPLserializer(serializers.ModelSerializer):

    class Meta:
        model = IPL
        fields = "__all__"