from ast import Try
import email
from email import utils
from random import random
from unittest.util import _MAX_LENGTH
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from notification.utils import Util
from notification.models import Smtpconfigure
from django.template import loader
from accounts.models import User
from django.http import JsonResponse
from configuration.models import Configurationtable,RoleConfiguration,Templatestable
from configuration.serializer import Configurationtableserializer
from access.views import Common
from log.models import UserLogin
from datetime import datetime
from access.models import RolesPermissions,AccessUserRoles,UserRoleMapping
from master.models import Designation, Unit, DataAccess
from django.template import Context, Template
from django.shortcuts import render
import requests
from access.serializer import UserRoleMappingSerializer,Processserializer
from master.serializer import DesignationSerializer, UnitSerializer, DataAccessSerializer
from NavyTrials.encryption import AESify
aes = AESify(block_len=16, salt_len=4)
from transaction import models as transactionModels
from master import models as masterModels

class MyTokenObtainSerializer(TokenObtainPairSerializer):

    permission_classes = (AllowAny,)
    loginname = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)
    fpdata = serializers.CharField(max_length= 255, required = True)
    #verification_code = serializers.CharField(max_length= 6)

    default_error_messages = {
        'Error': 'Incorrect username or password'
    }
    def to_internal_value(self, data):
        #print("test")
        loginname = data.get('loginname')
        password = (data.get('password'))
        #print(password)
        """
        Validate Password.
        """
        if not password or not loginname:
            raise serializers.ValidationError({'status':'error','message': 'Incorrect username or password'})
        return data
        
            
    def validate(self,  attrs):
        try:
         attrs._mutable = True
        except:
            print("12344")
        # try:
        attrs['password'] = aes.decrypt(attrs['password'])
        # except:
        #     attrs['password'] = (attrs['password'])
        
        data = super().validate(attrs)
        if data == 'False':
            return {'status': 'Error', "message" : "Incorrect username or password"}

        log_browser=self.context['request'].user_agent.browser.family
        log_version=self.context['request'].user_agent.browser.version_string
        log_os=self.context['request'].user_agent.os.family
        log_platform=self.context['request'].user_agent.device.family
        log_ip=Common.get_client_ip(self.context['request'])
        log_datetime = datetime.now()
            
        refresh = self.get_token(self.user)

        list=UserRoleMapping.objects.filter(user_id=self.user.id)
        roleSerializer=UserRoleMappingSerializer(list, many=True)
        designation=masterModels.Unit.objects.values('id','name','code').filter(id=self.user.desig_id)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_id'] = self.user.id
        data['designation'] = designation if designation else None
        data['role_center'] = roleSerializer.data
        data['user_email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['process_id'] = 1


        userlog=UserLogin.objects.create(user_id=self.user.id,logon_type='login',log_datetime=log_datetime,log_ip=log_ip,log_browser=log_browser,log_version=log_version,log_os=log_os,log_platform=log_platform).save()
        
        user_fields = {'loginname' : self.user.loginname, 'email' : self.user.email }

        configList = Configurationtable.objects.filter(status=1)
        configuration = Configurationtableserializer(configList, many=True)
        data['configuration'] = configuration.data

        ## Hierarchy ##

        ## Form ##
        formLevelRecommender = transactionModels.FormLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level').filter(recommender_id = self.user.id)

        formLevelApprover = transactionModels.FormLevelApproverHierarchy.objects.values('form','approver','approver_level').filter(approver_id = self.user.id)

        ## Project ##
        projectLevelRecommender = transactionModels.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level').filter(recommender_id = self.user.id)

        projectLevelApprover = transactionModels.ProjectLevelApproverHierarchy.objects.values('form','approver','approver_level').filter(approver_id = self.user.id)

        ## Initiator ##
        projectLevelRecommender = transactionModels.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level').filter(recommender_id = self.user.id)

        projectLevelApprover = transactionModels.ProjectLevelApproverHierarchy.objects.values('form','approver','approver_level').filter(approver_id = self.user.id)

        data['form_level_approver'] = formLevelApprover
        data['form_level_recommender'] = formLevelRecommender


        data['project_level_approver'] = projectLevelApprover
        data['project_level_recommender'] = projectLevelRecommender

        return data 
    
class MyTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_name=decoded_payload['loginname']
        # add filter query
        data.update({'user': self.user.user_name})
        return data


class DataAccessFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = transactionModels.DataAccessForms
        fields = "__all__"

class UserListSerializer(serializers.ModelSerializer):
    process = Processserializer (read_only=True)
    #designation = DesignationSerializer(read_only=True)
    class Meta:
        model = User
        fields = "__all__"        

    def to_representation(self, instance, appointment_id=None):        
        response = super().to_representation(instance)
        response['roles']=UserRoleMappingSerializer(UserRoleMapping.objects.filter(user_id=response['id']),many=True).data
        #response['designation'] = DesigationSerializer(Designation.objects.filter(id=response['desig']),many=True).data
        response['designation'] = UnitSerializer(Unit.objects.filter(id=response['desig']),many=True).data
        
        response['data_access']=DataAccessFormSerializer(transactionModels.DataAccessForms.objects.filter(user_id=response['id']),many=True).data  
        return response


class UserListHierarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","loginname"]