from logging import critical
from tabnanny import verbose
from django.db import models
from django.db.models.deletion import CASCADE
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User
from access.models import AccessUserRoles
from NavyTrials import settings

class Countries(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)    
    phone_code =models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    sequence = models.IntegerField(null=True, blank=True)
    status = models.SmallIntegerField(choices=((1, 'Active'), (2, 'Inactive'), (3, 'Delete')), default= 1)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now = True,  blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField( blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.countries'
        verbose_name = "Countries"
        verbose_name_plural = "Countries"

class Region(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.region'
        verbose_name = 'region'
        verbose_name_plural = 'region'  


class States(models.Model):

    name = models.CharField(max_length= 100)
    code = models.CharField(max_length=15)
    country = models.ForeignKey(Countries, on_delete= models.CASCADE)
    region = models.ForeignKey(Region, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1, 'Active'), (2, 'Inactive'), (3, 'Delete')))
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now = True,  blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.states'
        verbose_name = "States"
        verbose_name_plural = "States"


class Cities(models.Model):

    name = models.CharField(max_length= 100)
    code = models.CharField(max_length=15)
    state = models.ForeignKey(States, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1, 'Active'), (2, 'Inactive'), (3, 'Delete')) )
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now = True,  blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.cities'
        verbose_name = "Cities"
        verbose_name_plural = "Cities"                         


class LookupType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.lookup_type' 
        verbose_name = "Lookup Type"
        verbose_name_plural = "Lookup Type" 


class Lookup(models.Model):
    type = models.ForeignKey(LookupType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status =     models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by =  models.CharField(max_length=100)
    created_ip =  models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.lookup' 
        verbose_name = "Lookup"
        verbose_name_plural = "Lookup" 


# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     code = models.CharField(max_length=15)
#     sequence = models.IntegerField(null=True)
#     status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     created_ip = models.GenericIPAddressField()
#     modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
#     modified_by = models.CharField(max_length=100, blank=True, null=True)
#     modified_ip = models.GenericIPAddressField(blank=True, null=True) 

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'master.project'
#         verbose_name = 'project'
#         verbose_name_plural = 'project' 

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    #project_id = models.ForeignKey(Project, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.class'
        verbose_name = 'class'
        verbose_name_plural = 'class'

class ProjectType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.project_type'
        verbose_name = 'project_type'
        verbose_name_plural = 'project_type'


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)

    project_level = models.CharField(max_length=15, blank=True)
    project_level_id = models.CharField(max_length=15, blank=True)
    project_level_name = models.CharField(max_length=15, blank=True)
    project_type = models.ForeignKey(ProjectType, on_delete= models.CASCADE,null=True)
    class_id = models.ForeignKey(Class, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.project'
        verbose_name = 'project'
        verbose_name_plural = 'project' 


class RefitType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.refit_type'
        verbose_name = 'refit_type'
        verbose_name_plural = 'refit_type'


class Defect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)

    dl_1 = models.CharField(max_length=15, blank=True, null=True)
    dl_2 = models.CharField(max_length=15, blank=True, null=True)
    dl_3 = models.CharField(max_length=15, blank=True, null=True)
    sdl = models.CharField(max_length=15, blank=True, null=True)

    awrf_1 = models.CharField(max_length=15, blank=True, null=True)
    awrf_2 = models.CharField(max_length=15, blank=True, null=True)
    awrf_3 = models.CharField(max_length=15, blank=True, null=True)

    refit_type = models.ForeignKey(RefitType, on_delete= models.CASCADE, blank=True, null=True)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.defect_list'
        verbose_name = 'defect_list'
        verbose_name_plural = 'defect_list'



class DefectListRefitType(models.Model):

    defect = models.ForeignKey(Defect, on_delete= models.CASCADE)
    refit_type = models.ForeignKey(RefitType, on_delete= models.CASCADE)

    def __str__(self):
        return self.defect

    class Meta:
        db_table = 'master.defect_list_refit_type'
        verbose_name = 'defect_list_refit_type'
        verbose_name_plural = 'defect_list_refit_type'


class Command(models.Model):
    CommandID = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.command'
        verbose_name = 'command'
        verbose_name_plural = 'command' 

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.department'
        verbose_name = 'department'
        verbose_name_plural = 'department'

class Section(models.Model):
    SectionID = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)    
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.section'
        verbose_name = 'section'
        verbose_name_plural = 'section'

class SubSection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    section_id = models.ForeignKey(Section, on_delete= models.CASCADE)
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.sub_section'
        verbose_name = 'sub_section'
        verbose_name_plural = 'sub_section'


class UnitType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.unit_type'
        verbose_name = 'unit_type'
        verbose_name_plural = 'unit_type'

class Unit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    #command_id = models.ForeignKey(Command, on_delete= models.CASCADE)
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete= models.CASCADE)
    unit_type_id = models.ForeignKey(UnitType, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.unit'
        verbose_name = 'unit'
        verbose_name_plural = 'unit'

class Authority(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.authority'
        verbose_name = 'authority'
        verbose_name_plural = 'authority'


class Ship(models.Model):
    ShipID = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    command_id = models.ForeignKey(Command, on_delete= models.CASCADE)
    #class_id = models.ForeignKey(Class, on_delete= models.CASCADE, null=True)
    #project_id = models.ForeignKey(Project, on_delete= models.CASCADE, null=True)
    #authority_id = models.ForeignKey(Authority, on_delete= models.CASCADE, null=True)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.ship'
        verbose_name = 'ship'
        verbose_name_plural = 'ship'
## Module and Sub Module

class Module(models.Model):
    name = models.TextField(null=True, blank=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.module'
        verbose_name = 'module'
        verbose_name_plural = 'module'

class SubModule(models.Model):
    name = models.TextField(null=True, blank=True)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    targetted_month_moderate = models.IntegerField(null=True)
    targetted_month_complex = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.sub_module'
        verbose_name = 'sub_module'
        verbose_name_plural = 'sub_module'


# Global Section
class GlobalSection(models.Model):
    Class = models.ForeignKey(Class,on_delete=models.CASCADE,default=13)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    section_no = models.CharField(max_length=30)
    sequence = models.IntegerField(null=True)
    data_type = models.SmallIntegerField(choices=((1,'editor'),(2,'datepicker'),(3,'number'),(4,'dropdown')),default=1)
    default_values = models.CharField(max_length=100, blank=True, null=True)
    type_general = models.IntegerField(null=True)
    type_system = models.IntegerField(null=True)
    type_equipment = models.IntegerField(null=True)
    type_compartment = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.global_section'
        verbose_name = 'global_section'
        verbose_name_plural = 'global_section'


class GlobalSubSection(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    global_section = models.ForeignKey(GlobalSection, on_delete= models.CASCADE)
    section_no = models.CharField(max_length=30)
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    data_type = models.SmallIntegerField(choices=((1,'editor'),(2,'datepicker'),(3,'number'),(4,'dropdown')),default=1)
    default_values = models.CharField(max_length=100, blank=True, null=True)
    type_general = models.IntegerField(null=True)
    type_system = models.IntegerField(null=True)
    type_equipment = models.IntegerField(null=True)
    type_compartment = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.global_sub_section'
        verbose_name = 'global_sub_section'
        verbose_name_plural = 'global_sub_section'

class GlobalSubSubSection(models.Model):
    #name = models.CharField(max_length=100, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    global_section = models.ForeignKey(GlobalSection, on_delete= models.CASCADE)
    global_sub_section = models.ForeignKey(GlobalSubSection, on_delete= models.CASCADE)
    section_no = models.CharField(max_length=30)
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    data_type = models.SmallIntegerField(choices=((1,'editor'),(2,'datepicker'),(3,'number'),(4,'dropdown')),default=1)
    default_values = models.CharField(max_length=100, blank=True, null=True)
    type_general = models.IntegerField(null=True)
    type_system = models.IntegerField(null=True)
    type_equipment = models.IntegerField(null=True)
    type_compartment = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.global_sub_sub_section'
        verbose_name = 'global_sub_sub_section'
        verbose_name_plural = 'global_sub_sub_section'

#######

class Compartment(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    # global_section = models.ForeignKey(GlobalSection,null=True, on_delete= models.CASCADE)
    # global_sub_section = models.ForeignKey(GlobalSubSection,null=True, on_delete= models.CASCADE)
    # global_sub_sub_section= models.ForeignKey(GlobalSubSubSection,null=True, on_delete= models.CASCADE)
    class_id = models.ForeignKey(Class, null=True, on_delete= models.CASCADE)
    section_id = models.ForeignKey(Section, null=True, on_delete= models.CASCADE,blank=True)
    #department_id = models.ForeignKey(Department, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.compartment'
        verbose_name = 'compartment'
        verbose_name_plural = 'compartment'

class System(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    section_id = models.ForeignKey(Section, null=True, on_delete= models.CASCADE)
    # global_section = models.ForeignKey(GlobalSection,null=True, on_delete= models.CASCADE)
    # global_sub_section = models.ForeignKey(GlobalSubSection,null=True, on_delete= models.CASCADE)
    # global_sub_sub_section= models.ForeignKey(GlobalSubSubSection,null=True, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.system'
        verbose_name = 'system'
        verbose_name_plural = 'system'


class Equipment(models.Model):
    EquipmentID = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    equipment_type_name = models.CharField(max_length=15, null=True, blank=True)
    system_id = models.ForeignKey(System, null=True, on_delete= models.CASCADE)
    section_id = models.ForeignKey(Section, null=True, on_delete= models.CASCADE)
    #global_section = models.ForeignKey(GlobalSection,null=True, on_delete= models.CASCADE)
    #global_sub_section = models.ForeignKey(GlobalSubSection,null=True, on_delete= models.CASCADE)
    #global_sub_sub_section= models.ForeignKey(GlobalSubSubSection,null=True, on_delete= models.CASCADE)
    #equipment_ship_id = models.IntegerField(null=True)
    equipment_ship_id = models.CharField(max_length=100, blank=True, null=True)
    sequence = models.IntegerField(null=True)

    # New Fields
    #equipment_model = models.CharField(max_length=100, blank=True, null=True)
    equipment_model = models.CharField(max_length=100, blank=True, null=True)
    nomenclature = models.TextField(null=True, blank=True)
    esd_equipment_id = models.CharField(max_length=100, blank=True, null=True) #??? master
    #ship_id = models.CharField(max_length=100, blank=True, null=True) #??? master
    ship = models.ForeignKey(Ship, null=True, on_delete= models.CASCADE)
    universal_id_m_ship = models.CharField(max_length=100, blank=True, null=True) #???
    #equipment_sr_no = models.CharField(max_length=100, blank=True, null=True) #???
    equipment_sr_no = models.TextField(null=True, blank=True)
    # New Fields

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.equipment'
        verbose_name = 'equipment'
        verbose_name_plural = 'equipment'

class UnitCompartment(models.Model):
    unit = models.ForeignKey(Unit, on_delete= models.CASCADE)
    compartment = models.ForeignKey(Compartment, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'mapping.unit_compartment'
        verbose_name = 'unit_compartment'
        verbose_name_plural = 'unit_compartment'

class UnitSystem(models.Model):
    unit = models.ForeignKey(Unit, on_delete= models.CASCADE)
    system = models.ForeignKey(System, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'mapping.unit_system'
        verbose_name = 'unit_system'
        verbose_name_plural = 'unit_system'

class UnitEquipments(models.Model):
    unit = models.ForeignKey(Unit, on_delete= models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'mapping.unit_equipment'
        verbose_name = 'unit_equipment'
        verbose_name_plural = 'unit_equipment'

class GlobalStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    is_completed = models.SmallIntegerField(default = 2, choices = ((1,'Yes'),(2,'No')))
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.global_status'
        verbose_name = 'global_status'
        verbose_name_plural = 'global_status'


class Designation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.designation'
        verbose_name = 'designation'
        verbose_name_plural = 'designation'







class Template(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.template'
        verbose_name = 'template'
        verbose_name_plural = 'template'



class TemplateConfigMaster(models.Model):

    template = models.ForeignKey(Template, on_delete=models.CASCADE,null=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.paragraph_title

    class Meta:
        db_table = 'master.template_config_master'
        verbose_name = 'Template Config Master'
        verbose_name_plural = 'Template Config Master'


class TemplateConfig(models.Model):

    template_config_master = models.ForeignKey(TemplateConfigMaster, on_delete=models.CASCADE,null=True)
    template = models.ForeignKey(Template, on_delete = models.CASCADE)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    sub_module =  models.ForeignKey(SubModule, on_delete = models.CASCADE)

    section_type = models.CharField(max_length=15, null=True, blank=True)
    section_value = models.CharField(max_length=15, null=True, blank=True)
    compartment_value = models.CharField(max_length=15, null=True, blank=True)
    selection_from = models.CharField(max_length=15, null=True, blank=True)
    selection_to = models.CharField(max_length=15, null=True, blank=True)

    sub_section_type = models.CharField(max_length=15, null=True, blank=True)
    sub_section_value = models.CharField(max_length=15, null=True, blank=True)
    sub_compartment_value = models.CharField(max_length=15, null=True, blank=True)
    sub_selection_from = models.CharField(max_length=15, null=True, blank=True)
    sub_selection_to = models.CharField(max_length=15, null=True, blank=True)

    sub_sub_section_type = models.CharField(max_length=15, null=True, blank=True)
    sub_sub_section_value = models.CharField(max_length=15, null=True, blank=True)
    sub_sub_compartment_value = models.CharField(max_length=15, null=True, blank=True)
    sub_sub_selection_from = models.CharField(max_length=15, null=True, blank=True)
    sub_sub_selection_to = models.CharField(max_length=15, null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.template_config'
        verbose_name = 'template_config'
        verbose_name_plural = 'template_config'


class DataAccess(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    # sub_module = models.ForeignKey(
    #     SubModule, on_delete=models.CASCADE, null=True
    # )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "access.data_access"
        verbose_name = "Data Access"
        verbose_name_plural = "Data Access"
        #unique_together = ("user", "module", "sub_module")
        unique_together = ("user", "module")

class DataAccessSubModule(models.Model):
    data_access = models.ForeignKey(DataAccess, on_delete=models.CASCADE, null=True)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.data_access

    class Meta:
        db_table = "access.data_access_sub_module"
        verbose_name = "Data Access Sub Module"
        verbose_name_plural = "Data Access Sub Module"



class Ships(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    #command_id = models.ForeignKey(Command, on_delete= models.CASCADE)
    Class = models.ForeignKey(Class, on_delete= models.CASCADE)
    project = models.ForeignKey(Project, on_delete= models.CASCADE)
    #authority_id = models.ForeignKey(Authority, on_delete= models.CASCADE)
    #sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.ships'
        verbose_name = 'ships'
        verbose_name_plural = 'ships'

############################

class Dockyard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    command_id = models.ForeignKey(Command, on_delete= models.CASCADE)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.dockyard'
        verbose_name = 'dockyard'
        verbose_name_plural = 'dockyard'

class DockyardGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.dockyard_group'
        verbose_name = 'dockyard_group'
        verbose_name_plural = 'dockyard_group'


class DockyardSubGroup(models.Model):
    dockyard = models.ForeignKey(Dockyard, on_delete= models.CASCADE)
    dockyard_group = models.ForeignKey(DockyardGroup, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.dockyard_sub_group'
        verbose_name = 'dockyard_sub_group'
        verbose_name_plural = 'dockyard_sub_group'


class Center(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete= models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.center'
        verbose_name = 'center'
        verbose_name_plural = 'center'


class Shopfloor(models.Model):
    center = models.ForeignKey(Center, on_delete= models.CASCADE)
    dockyard_sub_group = models.ForeignKey(DockyardSubGroup, on_delete= models.CASCADE)
    section = models.ForeignKey(Section, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.shopfloor'
        verbose_name = 'shopfloor'
        verbose_name_plural = 'shopfloor'
        
class CategoryType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.categorytype'
        verbose_name = 'categorytype'
        verbose_name_plural = 'categorytype'

class PayScale(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.payscale'
        verbose_name = 'payscale'
        verbose_name_plural = 'payscale'


# class DemandMaster(models.Model):
#     qty = models.CharField(max_length=100)
#     code = models.CharField(max_length=15)
#     # code = models.CharField(max_length=15) 
#     demand_date = models.DateTimeField(null=True)
#     center_no = models.ForeignKey(Center, on_delete= models.CASCADE)
#     # wi_number =models.ForeignKey(settings.WorkInstruction_MODEL,on_delete=models.CASCADE,null=True)
#     # wi_number = models.ForeignKey(WorkInstruction, on_delete=models.CASCADE, null=True,  related_name='dm_work_instruction')
#     status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     created_ip = models.GenericIPAddressField()
#     modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
#     modified_by = models.CharField(max_length=100, blank=True, null=True)
#     modified_ip = models.GenericIPAddressField(blank=True, null=True) 

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'master.demand_master'
#         verbose_name = 'demand_master'
#         verbose_name_plural = 'demand_master'

class ItemsMaster(models.Model):
    code = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    item_type_id = models.CharField(max_length=15, blank=True)
    min_stock_level = models.CharField(max_length=15, blank=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.items_master'
        verbose_name = 'items_master'
        verbose_name_plural = 'items_master'




