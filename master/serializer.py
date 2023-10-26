from socketserver import DatagramRequestHandler
from venv import create
from django.db.models import F
from rest_framework import serializers
from .models import Countries, States, Cities,LookupType,Lookup,Region,Dockyard,Command
from access.serializer import AccessUserRoleserializer
from . import models
from NavyTrials import settings

class Countriesserializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = "__all__"
         
class Regionserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Region
        fields = "__all__"       

class ListRegionserializer(serializers.ModelSerializer):
    
    country = Countriesserializer(read_only=True)
    class Meta:
        model = Region
        fields = "__all__"            

class ListStatesserializer(serializers.ModelSerializer):
    country = Countriesserializer(read_only=True)
    region = Regionserializer(read_only=True)

    class Meta:
        model = States
        fields = "__all__"

class Statesserializer(serializers.ModelSerializer):

    class Meta:
        model = States
        fields = "__all__"        

    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
    

class ListCitiesserializer(serializers.ModelSerializer):
    state = Statesserializer(read_only=True)

    class Meta:
        model = Cities
        fields = "__all__" 

class Citiesserializer(serializers.ModelSerializer):

    class Meta:
        model = Cities
        fields = "__all__" 

class LookupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupType
        fields = "__all__"  

class ListLookupSerializer(serializers.ModelSerializer):
    type = LookupTypeSerializer(read_only=True)
    
    class Meta:
        model = Lookup
        fields = "__all__"

class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookup
        fields = "__all__"

class ClassSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Class
        fields = "__all__"       
        # fields = ['id','name']

class ListClassSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Class
        fields = "__all__"

class CommandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Command
        fields = "__all__"       

class ListCommandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Command
        fields = "__all__" 


class ListDockyardSerializer(serializers.ModelSerializer):
    command_id = CommandSerializer(read_only = True)
    #project_id = projectSerializer(read_only=True)
    class Meta:
        model = models.Dockyard
        fields = "__all__" 

class DockyardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Dockyard
        fields = "__all__"       
        #fields = ['id','name']

# class ListDockyardSerializer(serializers.ModelSerializer):
    
#     #project_id = projectSerializer(read_only=True)
#     class Meta:
#         model = models.Class
#         fields = "__all__" 
      

class ProjectTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ProjectType
        fields = "__all__"       

class ListProjectTypeSerializer(serializers.ModelSerializer):
    
    class_id = ClassSerializer(read_only=True)
    class Meta:
        model = models.ProjectType
        fields = "__all__" 

class projectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Project
        fields = "__all__"       

class ListProjectSerializer(serializers.ModelSerializer):
    
    class_id = ClassSerializer(read_only=True)
    class Meta:
        model = models.Project
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        project_type_id = response['project_type']
        response['project_type_det'] = models.ProjectType.objects.values('id','name','code').filter(id=project_type_id).first()
        return response


class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Department
        fields = "__all__"       

class ListDepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Department
        fields = "__all__" 

class SectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Section
        fields = "__all__"       

class ListSectionSerializer(serializers.ModelSerializer):
    
    department_id = DepartmentSerializer(read_only=True)
    class Meta:
        model = models.Section
        fields = "__all__" 

class SubSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.SubSection
        fields = "__all__"       

class ListSubSectionSerializer(serializers.ModelSerializer):

    section_id = SectionSerializer(read_only=True)
    department_id = DepartmentSerializer(read_only=True)
    class Meta:
        model = models.SubSection
        fields = "__all__" 

class UnitTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UnitType
        fields = "__all__"       

class ListUnitTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UnitType
        fields = "__all__" 

class UnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Unit
        fields = "__all__"       

class ListUnitSerializer(serializers.ModelSerializer):

    command_id = CommandSerializer(read_only=True)
    section_id = SectionSerializer(read_only=True)
    department_id = DepartmentSerializer(read_only=True)
    unit_type_id = UnitTypeSerializer(read_only=True)

    class Meta:
        model = models.Unit
        fields = "__all__" 

class AuthoritySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Authority
        fields = "__all__"       

class ListAuthoritySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Authority
        fields = "__all__" 



class ShipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Ship
        fields = "__all__"       

class ListShipSerializer(serializers.ModelSerializer):

    command_id = CommandSerializer(read_only=True)
    class_id = ClassSerializer(read_only=True)
    project_id = projectSerializer(read_only=True)
    authority_id = AuthoritySerializer(read_only=True)

    class Meta:
        model = models.Ship
        fields = "__all__" 


class ShipsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Ships
        fields = "__all__"       

class ListShipsSerializer(serializers.ModelSerializer):

    #command_id = CommandSerializer(read_only=True)
    Class = ClassSerializer(read_only=True)
    project = projectSerializer(read_only=True)
    #authority_id = AuthoritySerializer(read_only=True)

    class Meta:
        model = models.Ships
        fields = "__all__" 

# Module and Sub Module

class ModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Module
        #fields = "__all__"
        fields = ['id', 'name']


class ListModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Module
        fields = "__all__" 

class SubModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.SubModule
        fields = "__all__"
        #fields = ['id', 'name']

class ListSubModuleSerializer(serializers.ModelSerializer):

    module = ModuleSerializer(read_only = True)
    class Meta:
        model = models.SubModule
        fields = "__all__" 

# Global
class GlobalSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalSection
        #fields = "__all__"
        fields = ['id', 'name']

class ListGlobalSectionSerializer(serializers.ModelSerializer):
    Class=ClassSerializer(read_only=True)
    module = ModuleSerializer(read_only = True)
    sub_module = SubModuleSerializer(read_only = True)
    class Meta:
        model = models.GlobalSection
        fields = "__all__" 

class GlobalSubSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalSubSection
        #fields = "__all__" 
        fields = ['id', 'name']      

class ListGlobalSubSectionSerializer(serializers.ModelSerializer):

    global_section = GlobalSectionSerializer(read_only=True)
    module = ModuleSerializer(read_only = True)
    sub_module = SubModuleSerializer(read_only = True)

    class Meta:
        model = models.GlobalSubSection
        fields = "__all__" 


class GlobalSubSubSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalSubSubSection
        #fields = "__all__"    
        fields = ['id', 'name']   

class ListGlobalSubSubSectionSerializer(serializers.ModelSerializer):

    global_section = GlobalSectionSerializer(read_only=True)
    global_sub_section = GlobalSubSectionSerializer(read_only=True)
    module = ModuleSerializer(read_only = True)
    sub_module = SubModuleSerializer(read_only = True)

    class Meta:
        model = models.GlobalSubSubSection
        fields = "__all__" 

class CompartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Compartment
        fields = "__all__"       

class ListCompartmentSerializer(serializers.ModelSerializer):

    # command_id = CommandSerializer(read_only=True)  
    class_id = ClassSerializer(read_only=True)
    section_id = SectionSerializer(read_only=True)
    # department_id = DepartmentSerializer(read_only=True)
    global_section = GlobalSectionSerializer(read_only=True)
    global_sub_section = GlobalSubSectionSerializer(read_only=True)
    global_sub_sub_section = GlobalSubSectionSerializer(read_only=True)
    class Meta:
        model = models.Compartment
        fields = "__all__" 

class SystemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.System
        fields = "__all__"       

class ListSystemSerializer(serializers.ModelSerializer):
    section_id = SectionSerializer(read_only=True)
    global_section = GlobalSectionSerializer(read_only=True)
    global_sub_section = GlobalSubSectionSerializer(read_only=True)
    global_sub_sub_section = GlobalSubSectionSerializer(read_only=True)
    class Meta:
        model = models.System
        fields = "__all__" 

class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Equipment
        fields = "__all__"       

class ListEquipmentSerializer(serializers.ModelSerializer):
    
    #system_id = SystemSerializer(read_only=True)
    # global_section = GlobalSectionSerializer(read_only=True)
    # global_sub_section = GlobalSubSectionSerializer(read_only=True)
    # global_sub_sub_section = GlobalSubSectionSerializer(read_only=True)
    class Meta:
        model = models.Equipment
        fields = "__all__" 


class GlobalStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalStatus
        fields = "__all__"       

class ListGlobalStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalStatus
        fields = "__all__" 


class DesignationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Designation
        fields = "__all__"       

class ListDesignationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Designation
        fields = "__all__" 


    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        personnel_type_id = response['personnel_type']
        response['personnel_type_det'] = models.PersonnelType.objects.values('id','name','code').filter(id=personnel_type_id).first()
        return response




class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Template
        fields = "__all__"

class ListTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Template
        fields = "__all__" 


class TemplateConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TemplateConfig
        fields = "__all__"

class ListTemplateConfigSerializer(serializers.ModelSerializer):

    template = TemplateSerializer(read_only = True)
    module = ModuleSerializer(read_only = True)
    sub_module = SubModuleSerializer(read_only = True)
    
    class Meta:
        model = models.TemplateConfig
        fields = "__all__" 


class ListTemplateConfigSerializer2(serializers.ModelSerializer):

    template = TemplateSerializer(read_only = True)
    module = ModuleSerializer(read_only = True)
    sub_module = SubModuleSerializer(read_only = True)
    
    class Meta:
        model = models.TemplateConfig
        fields = "__all__" 

class TemplateConfigMasterSerializer(serializers.ModelSerializer):

    template = TemplateSerializer(read_only = True)
    class Meta:
        model = models.TemplateConfigMaster
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        template_config_master = response['id']
        response['details'] = ListTemplateConfigSerializer2(models.TemplateConfig.objects.filter(template_config_master = template_config_master), many=True).data
        return response

class TemplateConfigMasterCURDSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TemplateConfigMaster
        fields = "__all__"


class TemplateGenerateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubModule
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        sub_module = response['id']
        response['section'] = ListGlobalSectionSerializer2(models.GlobalSection.objects.filter(sub_module = sub_module, status = 1).order_by('id'), many=True).data
        return response



class ListGlobalSectionSerializer2(serializers.ModelSerializer):

    #sub_module = SubModuleSerializer(read_only = True)
    class Meta:
        model = models.GlobalSection
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        #print(response,"uuuuuuuuuu")
        global_section = response['id']
        module = response['module']
        sub_module = response['sub_module']
        response['sub_section'] = ListGlobalSubSectionSerializer2(models.GlobalSubSection.objects.filter(module = module, sub_module = sub_module, global_section = global_section, status = 1), many=True).data
        return response


class ListGlobalSubSectionSerializer2(serializers.ModelSerializer):

    #global_section = GlobalSectionSerializer(read_only=True)
    #sub_module = SubModuleSerializer(read_only = True)

    class Meta:
        model = models.GlobalSubSection
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        #print(response,"uuuuuuuuuu")
        global_sub_section = response['id']
        global_section = response['global_section']
        module = response['module']
        sub_module = response['sub_module']
        response['sub_sub_section'] = ListGlobalSubSubSectionSerializer2(models.GlobalSubSubSection.objects.filter(module = module, sub_module = sub_module, global_section = global_section, global_sub_section = global_sub_section, status = 1), many=True).data
        return response


class ListGlobalSubSubSectionSerializer2(serializers.ModelSerializer):

    #global_section = GlobalSectionSerializer(read_only=True)
    #global_sub_section = GlobalSubSectionSerializer(read_only=True)
    #sub_module = SubModuleSerializer(read_only = True)

    class Meta:
        model = models.GlobalSubSubSection
        fields = "__all__" 


# class GlobalSubSectionSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.GlobalSubSection
#         fields = "__all__"`



# class GlobalTransactionDetailsSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.GlobalTransactionDetails
#         fields = "__all__"


# class ListGlobalTransactionDetailsSerializer(serializers.ModelSerializer):

#     global_transaction = GlobalSectionSerializer(read_only=True)
#     sub_module = SubModuleSerializer(read_only = True)

#     class Meta:
#         model = models.GlobalSubSection
#         fields = "__all__" 


class DataAccessSubModuleSerializer(serializers.ModelSerializer):
    sub_module=SubModuleSerializer(read_only=True)

    class Meta:
        model = models.DataAccessSubModule
        fields = "__all__"

class DataAccessSerializerCRUD(serializers.ModelSerializer):
    class Meta:
        model = models.DataAccess
        fields = "__all__"

class DataAccessSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    sub_module = SubModuleSerializer(read_only=True)
    #ship=ShipsSerializer(read_only=True)
   
    class Meta:
        model = models.DataAccess
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        data_access_id=response['id']
        #response['ships']=DataAccessShipSerializer(models.DataAccessShip.objects.filter(data_access_id=data_access_id),many=True).data
        response['sub_module']=DataAccessSubModuleSerializer(models.DataAccessSubModule.objects.filter(data_access_id=data_access_id),many=True).data
        return response


#### DockYard ####

class RefitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RefitType
        fields = "__all__"       

class ListRefitTypeSerializer(serializers.ModelSerializer):
    
    #class_id = ClassSerializer(read_only=True)
    class Meta:
        model = models.RefitType
        fields = "__all__"


class DefectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Defect
        fields = "__all__"       

class ListDefectSerializer(serializers.ModelSerializer):
    
    #class_id = ClassSerializer(read_only=True)
    class Meta:
        model = models.Defect
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        refit_type_id = response['refit_type']
        response['refit_type_det'] = models.RefitType.objects.values('id','name','code').filter(id=refit_type_id).first()
        return response

class ListDockyardGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DockyardGroup
        fields = "__all__" 

class DockyardGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DockyardGroup
        fields = "__all__"


class ListDockyardSubGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DockyardSubGroup
        fields = "__all__" 

class DockyardSubGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DockyardSubGroup
        fields = "__all__"

class CenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Center
        fields = "__all__"

class ListCenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Center
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        equipment_id = response['equipment']
        response['equipment_det'] = models.Equipment.objects.values('id','name','code').filter(id=equipment_id).first()
        return response

class ShopfloorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Shopfloor
        fields = "__all__"

class ListShopfloorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Shopfloor
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        center_id = response['center']
        response['center_det'] = models.Center.objects.values('id','name','code').filter(id=center_id).first()
        return response

class CategoryTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CategoryType
        fields = "__all__"       

class ListCategoryTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CategoryType
        fields = "__all__" 

class PayScaleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PayScale
        fields = "__all__"       

class ListPayScaleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PayScale
        fields = "__all__" 
class DemandMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DemandMaster
        fields = "__all__"       

class ListDemandMasterSerializer(serializers.ModelSerializer):
     
    # Center_id = CenterSerializer(read_only=True)
    # WI_id = WorkInstructionSerializer(read_only=True)


    class Meta:
        model = models.DemandMaster
        fields = "__all__" 



class ItemsMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ItemsMaster
        fields = "__all__"       


class ItemTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ItemType
        fields = "__all__"       

class ListItemTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ItemType
        fields = "__all__"

class ListItemsMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ItemsMaster
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        item_type_id = response['item_type']
        
        response['item_type_det'] = models.ItemType.objects.values('id','name',).filter(id=item_type_id).first()
        return response

class AllowancesMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AllowancesMaster
        fields = "__all__"       

class ListAllowancesMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AllowancesMaster
        fields = "__all__" 

class DeductionsMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DeductionsMaster
        fields = "__all__"       

class ListDeductionsMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DeductionsMaster
        fields = "__all__" 

class PayGradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PayGrade
        fields = "__all__"       

class ListPayGradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PayGrade
        fields = "__all__" 

class PersonnelTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PersonnelType
        fields = "__all__"       

class ListPersonnelTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PersonnelType
        fields = "__all__" 

class StatusMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.StatusMaster
        fields = "__all__"       

class ListStatusMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.StatusMaster
        fields = "__all__"

class RankSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Rank
        fields = "__all__"       

class ListRankSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Rank
        fields = "__all__" 
    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        pay_grade_id = response['pay_grade']
        personnel_type_id = response['personnel_type']
        response['pay_grade_det'] = models.PayGrade.objects.values('id','name',).filter(id=pay_grade_id).first()
        response['personnel_type_det'] = models.PersonnelType.objects.values('id','name',).filter(id=personnel_type_id).first()
        return response


class StorageLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.StorageLocation
        fields = "__all__"       

class ListStorageLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.StorageLocation
        fields = "__all__"

class IssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Issue
        fields = "__all__"       

class ListIssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Issue
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        
        demand_id= response['demand']
        
        response['demand_master_det'] = models.DemandMaster.objects.values('id','qty',).filter(id=demand_id).first()
        return response

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Course
        fields = "__all__"       

class ListCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Course
        fields = "__all__"

class BatchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Batch
        fields = "__all__"       

class ListBatchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Batch
        fields = "__all__"


class OverTimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.OverTime
        fields = "__all__"       

class ListOverTimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.OverTime
        fields = "__all__"


class HolidaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Holiday
        fields = "__all__"       

class ListHolidaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Holiday
        fields = "__all__"
