from rest_framework import serializers
from .models import Notification,Smtpconfigure,NotificationUser,NotificationUserLog
from access.serializer import AccessUserRoleserializer
from accounts.models import User
import re

class Smtpconfigureserializer(serializers.ModelSerializer):

    class Meta:
        model = Smtpconfigure
        fields = '__all__'


class NotificationUserSerializer(serializers.ModelSerializer):

    user_role = AccessUserRoleserializer(read_only=True)
    
    class Meta:
        model = NotificationUser
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     if self.context:
    #         response['trial']=TrialListSerializer((Trials.objects.filter(id=response['trial'])), many=True,context = (self.context if self.context else {'request':''})).data[0]
    #     return response



class Notificationserializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
       

    def to_representation(self, instance):
        response = super(Notificationserializer, self).to_representation(instance)
        if response['type'] ==1:
            regex = re.compile(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')
            if re.fullmatch(regex, response['to']) is not None:
                return response
            else:
                raise serializers.ValidationError("phone number invalid")   

        elif response['type'] ==2:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, response['to']) is not None:
                return response
            else:
                raise serializers.ValidationError("email invalid")    

 














            
        
            



    