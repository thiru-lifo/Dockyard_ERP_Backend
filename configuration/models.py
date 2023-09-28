from django.db import models

from master.models import Countries,Lookup
from access.models import AccessUserRoles
from accounts.models import User

class Configurationtable(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100,default='')
    default_values = models.TextField(default='', null=True)
    value = models.TextField(default='', null=True)
    code = models.CharField(max_length=100,default='')
    isCenter = models.BooleanField(default=False)
    status = models.SmallIntegerField(choices=((1, 'Active'), (2, 'Inactive'), (3, 'Delete')))
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'configuration.Configuration_table'
        verbose_name = "Configuration_table"
        verbose_name_plural = "Configuration_table"    


class RoleConfiguration(models.Model):
    config = models.ForeignKey(Configurationtable, on_delete= models.CASCADE) 
    role = models.ForeignKey(AccessUserRoles, on_delete= models.CASCADE) 

    def __str__(self):
        return self.config

    class Meta:
        db_table = 'configuration.role_configuration'
        verbose_name = "Center_Configuration"
        verbose_name_plural = "Center_Configuration"      

class Templatestable(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    type = models.SmallIntegerField(choices=((1,'Email'),(2,'PDF')),default=1,)
    actual_template = models.TextField(default='', null=True)
    modified_template = models.TextField(default='',null=True)
    modified_on = models.DateTimeField(auto_now=True , blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'configuration.templates'
        verbose_name = "common teamplate"
        verbose_name_plural = "Common Templates"

class TemplatesCountry(models.Model): 
    template = models.ForeignKey(Templatestable, on_delete = models.CASCADE)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    actual_template = models.TextField(default='', null=True)
    modified_template = models.TextField(default='',null=True)
    modified_on = models.DateTimeField(auto_now=True , blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.template   

    class Meta:
        db_table = 'configuration.templates_country'
        verbose_name = "teamplate_country"
        verbose_name_plural = "Template Countries"         


class Approval(models.Model):
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,null=True)
    level = models.SmallIntegerField(choices=((1,'First Level'),(2,'Second Level'),(3,'Three Level'),(4,'Fourth Level'),(5,'Fifth Level')),null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')),default=1)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name="created_by")
    created_ip = models.GenericIPAddressField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name="modified_by")
    modified_ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return self.user_role

    class Meta:
        db_table = 'configuration.approval' 
        verbose_name = "Approval"
        verbose_name_plural = "Approval"