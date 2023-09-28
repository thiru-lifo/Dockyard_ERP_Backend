from django.db import models
import accounts.models
import master.models
from NavyTrials import settings
#from master.models import Center
#from accounts.models import User

#from django.apps import apps
#Center = apps.get_model('master', 'Center')
#from master.models import Center
# Create your models here.

#from django.apps import apps
#Designation = apps.get_model('master', 'Designation')
#from master.models import Designation
#Create your models here.

#from master.models import Designation

class Process(models.Model):
    name = models.CharField(max_length=200)
    sequence = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.process' 
        verbose_name = "Process"
        verbose_name_plural = "Processes"

class Modules(models.Model):
    process =models.ForeignKey(Process,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=150)
    url = models.CharField(max_length=500,default='',null=True)
    icon = models.CharField(max_length=500,default='')
    sequence = models.IntegerField(null=True)
    action = models.TextField(blank=False, null=False)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.modules' 
        verbose_name = "Modules"
        verbose_name_plural = "Modules"

class ModulesComponents(models.Model):   
    name = models.CharField(max_length=200)
    module =models.ForeignKey(Modules,on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    sequence = models.IntegerField(null=True)
    url = models.CharField(max_length=500, null=True)
    icon = models.CharField(max_length=500,default='')
    action = models.TextField(blank=False, null=False)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.modules_components'  
        verbose_name = "ModulesComponents"
        verbose_name_plural = "ModulesComponents"

class ModulesComponentsAttributes(models.Model):
    name = models.CharField(max_length=200)   
    module_component =models.ForeignKey(ModulesComponents,on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    sequence = models.IntegerField(null=True)
    action = models.TextField(blank=False, null=False)
    url = models.CharField(max_length=500, null=True)
    icon = models.CharField(max_length=500,default='')
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.modules_components_attributes'  
        verbose_name = "Modules Components Attributes"
        verbose_name_plural = "Modules Components Attributes"        

class AccessUserRoles(models.Model):
    from_ad = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,default='')
    code = models.CharField(max_length=10,default='',unique=True)
    is_biometric=models.BooleanField(default=False)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 
    status = models.SmallIntegerField(default=1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.user_roles' 
        verbose_name = "Access User roles"
        verbose_name_plural = "Access User roles"

class ProcessRoleMapping(models.Model):
    process =models.ForeignKey(Process,on_delete=models.CASCADE,default=1)
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,default=1)
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.process_role_mapping' 
        verbose_name = "process_role_mapping"
        verbose_name_plural = "process_role_mapping"
        

class AccessModules(models.Model):
    module =models.ForeignKey(Modules,on_delete=models.CASCADE)
    module_components= models.ForeignKey(ModulesComponents, on_delete=models.CASCADE, blank=True, null=True)
    module_components_attribute= models.ForeignKey(ModulesComponentsAttributes, on_delete=models.CASCADE, blank=True, null=True)
    user_role= models.ForeignKey(AccessUserRoles, on_delete=models.CASCADE)
    action = models.TextField(blank=False, null=False)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by =  models.CharField(max_length=100)
    created_ip =  models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'access.access_modules' 
        verbose_name = "Access Modules"
        verbose_name_plural = "Access Modules"  

class Privileges(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=150)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by =  models.CharField(max_length=100)
    created_ip =  models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'access.privileges' 
        verbose_name = "Access Privileges"
        verbose_name_plural = "Access Privileges" 

class RolesPermissions(models.Model):
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,default=1)
    process =models.ForeignKey(Process,on_delete=models.CASCADE,default=1)
    permissions=models.TextField()
    def __str__(self):
        return self.permissions

    class Meta:
        db_table = 'access.roles_permission' 
        verbose_name = "Permission"
        verbose_name_plural = "Permissions" 

class UserRoleMapping(models.Model):
    process =models.ForeignKey(Process,on_delete=models.CASCADE,null=True,blank=True)
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,null=True)
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    default = models.SmallIntegerField(choices=((1,'Default center'),(0,'Non default')),null=True)
    
    def __str__(self):
        return self.user

    class Meta:
        db_table = 'access.user_role_mapping' 
        verbose_name = "User Role Mapping"
        verbose_name_plural = "Users Roles Mapping"
        unique_together = ('user_role', 'user') 


class ProcessFlow(models.Model):
    process =models.ForeignKey(Process,on_delete=models.CASCADE,default=1)
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,default=1)
    level=models.SmallIntegerField()

    def __str__(self):
        return self.permissions

    class Meta:
        db_table = 'access.process_flow' 
        verbose_name = "process_flow"
        verbose_name_plural = "process_flow" 



class UserRoleDesignation(models.Model):   

    
    user_role = models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE)
    
    #designation = models.ForeignKey(Designation,on_delete=models.CASCADE)
    designation = models.IntegerField(null=True)
    #user_role = models.ForeignKey(UserRole,on_delete=models.CASCADE)
    #designation = models.CharField(max_length=250)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.designation

    class Meta:
        db_table = 'access.user_role_designation'  
        verbose_name = "UserRoleDesignation"
        verbose_name_plural = "UserRoleDesignation"