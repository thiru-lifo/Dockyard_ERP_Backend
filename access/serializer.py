from os import access
from rest_framework import serializers
from django.db.models import CharField, Value,BooleanField
from django.db.models import Count, Case, When, IntegerField


from .models import  Modules, ModulesComponents, AccessUserRoles,AccessModules,ModulesComponentsAttributes,Privileges,RolesPermissions,Process,UserRoleMapping, UserRoleDesignation



class ListModulesserializer(serializers.ModelSerializer):

    class Meta:
        model = Modules
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','description','code','sequence').filter(id__in=action).exclude(status='3')
        return response         

class Modulesserializer(serializers.ModelSerializer):

    class Meta:
        model = Modules
        fields = "__all__"

class ListModulesComponentserializer(serializers.ModelSerializer):
    module = Modulesserializer(read_only=True)

    class Meta:
        model = ModulesComponents
        fields='__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','description','code','sequence').filter(id__in=action).exclude(status='3')
        module_action = response['module']['action'].strip('][').split(',')
        response['module']['action']=Privileges.objects.values('id','name','description','code','sequence').filter(id__in=module_action).exclude(status='3')
        return response    

class ModulesComponentserializer(serializers.ModelSerializer):
  
    class Meta:
        model = ModulesComponents
        fields='__all__' 

class ListModulesComponentsAttributeserializer(serializers.ModelSerializer):
    module_component = ModulesComponentserializer(read_only=True)

    class Meta:
        model = ModulesComponentsAttributes
        fields='__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','description','code','sequence').filter(id__in=action).exclude(status='3')
        module__component_action = response['module_component']['action'].strip('][').split(',')
        response['module_component']['action']=Privileges.objects.values('id','name','description','code','sequence').filter(id__in=module__component_action).exclude(status='3')
        return response       

class ModulesComponentsAttributeserializer(serializers.ModelSerializer):
    
    class Meta:
        model = ModulesComponentsAttributes
        fields='__all__'   

class AccessUserRoleserializer(serializers.ModelSerializer):

    class Meta:
        model = AccessUserRoles
        fields = "__all__"

class ListAccessModuleserializer(serializers.ModelSerializer):
    module = Modulesserializer (read_only=True)
    module_components = ModulesComponentserializer(read_only=True)
    module_components_attribute = ModulesComponentsAttributeserializer(read_only=True)
    user_role = AccessUserRoleserializer(read_only=True)

    class Meta:
        model = AccessModules
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','description','code','sequence').filter(id__in=action).exclude(status='3')
        module = response['module']['action'].strip('][').split(',')
        privileges = Privileges.objects.values('name','id').exclude(status='3')
        access_control =dict()
        if privileges:
            for x in privileges:
                if str(x['id']) in list(action):
                    access_control[x['name']] = True
                else:
                    access_control[x['name']] = False  
        response['access_conntrol'] = access_control   
        response['module']['action']=Privileges.objects.values('id','name','description','code','sequence').filter(id__in=module).exclude(status='3')
        if response['module_components']:
            module__component_action = response['module_components']['action'].strip('][').split(',')
            response['module_components']['action']=Privileges.objects.values('id','name','description','code','sequence').filter(id__in=module__component_action).exclude(status='3')
        if response['module_components_attribute']:
            module__component__attr_action = response['module_components_attribute']['action'].strip('][').split(',')
            response['module_components_attribute']['action']=Privileges.objects.values('id','name','description','code','sequence').filter(id__in=module__component__attr_action).exclude(status='3')
        return response    

class AccessModuleserializer(serializers.ModelSerializer):

    class Meta:
        model = AccessModules
        fields = "__all__"        

class Privilegesserializer(serializers.ModelSerializer):

    class Meta:
        model = Privileges
        fields = "__all__"


class AllAttributeserializer(serializers.ModelSerializer):

    class Meta:
        model = ModulesComponentsAttributes
        fields=["id","name","action","url"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','code').filter(id__in=action).exclude(status='3')
        return response 

class AllComponentserializer(serializers.ModelSerializer):
    class Meta:
        model = ModulesComponents
        fields=["id","name","action","url"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','code').filter(id__in=action).exclude(status='3')
        response['attributes']=AllAttributeserializer(ModulesComponentsAttributes.objects.filter(module_component_id=response['id']).exclude(status='3').order_by('sequence'),many=True).data
        return response  

class AllModulesserializer(serializers.ModelSerializer):

    class Meta:
        model = Modules
        fields = ["id","name","action","url"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        action = response['action'].strip('][').split(',')
        response['action'] = Privileges.objects.values('id','name','code').filter(id__in=action).exclude(status='3')
        response['components']=AllComponentserializer(ModulesComponents.objects.filter(module_id=response['id']).exclude(status='3').order_by('sequence'),many=True).data
        return response 

class Permissionsserializer(serializers.ModelSerializer):

    class Meta:
        model = RolesPermissions
        fields = "__all__"

class Processserializer(serializers.ModelSerializer):

    class Meta:
        model = Process
        fields = "__all__"




class UserRoleMappingSerializer(serializers.ModelSerializer):
    user_role = AccessUserRoleserializer(read_only=True)
    class Meta:
        model = UserRoleMapping
        fields = "__all__"   



class UserRoleDesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRoleDesignation
        fields = "__all__"

class UserRoleSerializer(serializers.ModelSerializer):



    user_role = UserRoleDesignationSerializer(read_only=True)

    class Meta:
        #model = UserRole
        model = AccessUserRoles
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        #action = response['action'].strip('][').split(',')
        #response['data_access'] = UserRoleDesignationSerializer['']
        response['data_access'] = UserRoleDesignationSerializer(UserRoleDesignation.objects.filter(user_role_id=response['id']),many=True).data  
        return response


