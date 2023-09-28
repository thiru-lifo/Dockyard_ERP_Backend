from rest_framework import serializers
from .models import Configurationtable,RoleConfiguration,TemplatesCountry,Templatestable,Approval
from master.serializer import Countriesserializer
from access.models import AccessUserRoles
from accounts.serializer import Userserializer

class Configurationtableserializer(serializers.ModelSerializer):

    class Meta:
        model = Configurationtable
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        isCenter = response['isCenter']
        response['role_detail'] =[]
                
        id = response['id']
        role_id = list(RoleConfiguration.objects.values('role_id').filter(config_id=id))
        role_dic =dict()
        for role in role_id: 
            role_val = AccessUserRoles.objects.values('id','name').filter(pk=role['role_id']).first()
            role_dic = {'id': role_val['id'],'name': role_val['name']}
            response['role_detail'].append(role_dic)
        return response    

class Templatestableserializer(serializers.ModelSerializer):
    class Meta:
        model = Templatestable
        fields = "__all__"

class TemplateCountryserializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatesCountry   
        fields = "__all__"

class ListTemplateCountryserializer(serializers.ModelSerializer):
    template = Templatestableserializer(read_only=True)
    country = Countriesserializer(read_only=True)

    class Meta:
        model = TemplatesCountry   
        fields = "__all__"
      

class AccessUserRoleserializer(serializers.ModelSerializer):
   
    class Meta:
        model = AccessUserRoles   
        fields = "__all__"

class ApprovalListSerializer(serializers.ModelSerializer):
    user_role =AccessUserRoleserializer(read_only=True)
    created_by=Userserializer(read_only=True)
    modified_by=Userserializer(read_only=True)

    class Meta:
        model = Approval   
        fields = "__all__"

class ApprovalSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Approval   
        fields = "__all__"