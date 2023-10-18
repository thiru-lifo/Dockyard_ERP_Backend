from socketserver import DatagramRequestHandler
from venv import create
from django.db.models import F
from rest_framework import serializers
from access.serializer import AccessUserRoleserializer
from accounts.models import User
from accounts import models as masterAccounts
from . import models
from accounts.serializer import Userserializer
from master.serializer import projectSerializer, ClassSerializer, ListProjectSerializer, UnitSerializer
from configuration.models import Approval
from master import models as masterModels
from master import serializer as masterSerializer

def getArrayValues(arrayString):
    import json
    import re
    try:
        return json.loads(re.sub("'", "\"", arrayString))
    except:
        return []

class PrimaryRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PrimaryRoles
        fields = "__all__"       

class ListPrimaryRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PrimaryRoles
        fields = "__all__" 

class SecondaryRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SecondaryRoles
        fields = "__all__"       

class ListSecondaryRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SecondaryRoles
        fields = "__all__" 

class StandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Standard
        fields = "__all__"       

class ListStandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Standard
        fields = "__all__" 

class PlanForManpowerInductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlanForManpowerInduction
        fields = "__all__"       

class ListPlanForManpowerInductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlanForManpowerInduction
        fields = "__all__" 

class AcquisitionMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AcquisitionMethod
        fields = "__all__"       

class ListAcquisitionMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AcquisitionMethod
        fields = "__all__" 


class SSSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SSS
        fields = "__all__"       

class ListSSSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SSS
        fields = "__all__" 


class PSRSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSection
        fields = "__all__"

class PSRSectionUnitSerializer(serializers.ModelSerializer):
    unit = masterSerializer.UnitSerializer(read_only=True)

    class Meta:
        model = models.PSRSectionUnit
        fields = "__all__"       

class ListPSRSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSection
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        section_id=response['id']
        response['units']=PSRSectionUnitSerializer(models.PSRSectionUnit.objects.filter(section_id=section_id),many=True).data
        return response


class PSRSectionUnitSerializer2(serializers.ModelSerializer):
    unit = masterSerializer.UnitSerializer(read_only=True)

    class Meta:
        model = models.PSRSectionUnit
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        section_unit_id=response['id']
        section_id=response['unit']['section_id']  
        response['compartments']=masterSerializer.CompartmentSerializer(masterModels.Compartment.objects.filter(section_id=section_id,status=1),many=True).data
        response['equipments']=masterSerializer.EquipmentSerializer(masterModels.Equipment.objects.filter(section_id=section_id,status=1),many=True).data
        response['systems']=masterSerializer.SystemSerializer(masterModels.System.objects.filter(section_id=section_id,status=1),many=True).data
        return response    

class PSRUnitCompartmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRUnitCompartments
        fields = "__all__"

class PSRUnitSystemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRUnitSystems
        fields = "__all__"

class PSRUnitEquipmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRUnitEquipments
        fields = "__all__"   

class ListPSRSectionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSection
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        section_id=response['id']
        response['units']=PSRSectionUnitSerializer2(models.PSRSectionUnit.objects.filter(section_id=section_id),many=True).data
        return response

class PSRSubSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSubSection
        fields = "__all__"       

class ListPSRSubSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSubSection
        fields = "__all__"




# GLS Master
class DocumentSectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentSections
        fields = "__all__"       

class ListDocumentSectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentSections
        fields = "__all__"

class DocumentSubSectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentSubSections
        fields = "__all__"       

class ListDocumentSubSectionsSerializer(serializers.ModelSerializer):

    document_sections = DocumentSectionsSerializer(read_only=True)

    class Meta:
        model = models.DocumentSubSections
        fields = "__all__"

class DocumentSubSections2Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentSubSections2
        fields = "__all__"       

class ListDocumentSubSections2Serializer(serializers.ModelSerializer):

    document_sections = DocumentSectionsSerializer(read_only=True)
    document_sub_sections = DocumentSubSectionsSerializer(read_only=True)

    class Meta:
        model = models.DocumentSubSections2
        fields = "__all__"

class AnnexuresSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Annexures
        fields = "__all__"       

class ListAnnexuresSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Annexures
        fields = "__all__"


# Initiation Notes
class InitiationNotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotes
        fields = "__all__"       

class ListInitiationNotesSerializer(serializers.ModelSerializer):

    standard = StandardSerializer(read_only=True)
    acquisition_method = AcquisitionMethodSerializer(read_only=True)
    plan_for_manpower_induction = PlanForManpowerInductionSerializer(read_only=True)
    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    pro_class = ClassSerializer(read_only=True)
    
    class Meta:
        model = models.InitiationNotes
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        primary_role=response['primary_role']
        secondary_role=response['secondary_role']
        response['primary_role']=[]
        response['secondary_role']=[]
        if primary_role:
            response['primary_role']=PrimaryRolesSerializer(models.PrimaryRoles.objects.filter(id__in=getArrayValues(primary_role)),many=True).data
        if secondary_role:
            response['secondary_role']=SecondaryRolesSerializer(models.SecondaryRoles.objects.filter(id__in=getArrayValues(secondary_role)),many=True).data
        return response

class ListALLInitiationNotesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.InitiationNotes
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        response['project'] = ListProjectSerializer(masterModels.Project.objects.filter(id=response['project']),many=True).data        
        return response


class InitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesDocument
        fields = "__all__"

class ListInitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesDocument
        fields = "__all__"

class InitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesSendMail
        fields = "__all__"

class ListInitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesSendMail
        fields = "__all__"


# PSR Formulation Of Approach Paper
class FormulationOfApproachPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaper
        fields = "__all__"       

class FormulationOfApproachPaperDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperDocument
        fields = "__all__"

class ListFormulationOfApproachPaperDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperDocument
        fields = "__all__"

class ListFormulationOfApproachPaperSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.FormulationOfApproachPaper
        fields = "__all__"




class FormulationOfApproachPaperSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperSendMail
        fields = "__all__"

class ListFormulationOfApproachPaperSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperSendMail
        fields = "__all__"


class FormulationOfApproachPaperResponsibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibility
        fields = "__all__"

class ListFormulationOfApproachPaperResponsibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibility
        fields = "__all__"


############
class FormulationOfApproachPaperResponsibilityCompartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilityCompartment
        fields = "__all__"

class ListFormulationOfApproachPaperResponsibilityCompartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilityCompartment
        fields = "__all__"


class FormulationOfApproachPaperResponsibilitySystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilitySystem
        fields = "__all__"

class ListFormulationOfApproachPaperResponsibilitySystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilitySystem
        fields = "__all__"

class FormulationOfApproachPaperResponsibilityEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilityEquipment
        fields = "__all__"

class ListFormulationOfApproachPaperResponsibilityEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormulationOfApproachPaperResponsibilityEquipment
        fields = "__all__"

# Presentation Of ApproachPaper
class PresentationOfApproachPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PresentationOfApproachPaper
        fields = "__all__"

class ListPresentationOfApproachPaperSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)

    class Meta:
        model = models.PresentationOfApproachPaper
        fields = "__all__"

# Presentation Of Approach Paper Send Mail
class PresentationOfApproachPaperSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PresentationOfApproachPaperSendMail
        fields = "__all__"

class ListPresentationOfApproachPaperSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PresentationOfApproachPaperSendMail
        fields = "__all__"

# Presentation Of Approach Paper Document
class PresentationOfApproachPaperDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PresentationOfApproachPaperDocument
        fields = "__all__"

class ListPresentationOfApproachPaperDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PresentationOfApproachPaperDocument
        fields = "__all__"



# PSR Inputs For Staff Requirement
class InputsForStaffRequirementSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.InputsForStaffRequirement
        fields = "__all__"

########################

class PSRDataFlowGeneralSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRDataFlowGeneralSection
        fields = "__all__"
#######################

class ListInputsForStaffRequirementSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    #project_id = PSRDataFlowGeneralSectionSerializer(read_only=True)
    
    class Meta:
        model = models.InputsForStaffRequirement
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        #print(response['project']['id'],"<--#########->")
        response['data_access'] = PSRDataFlowGeneralSectionSerializer(models.PSRDataFlowGeneralSection.objects.filter(project=response['project']['id']),many=True).data  
        return response


# Inputs For Staff Requirement Send Mail
class InputsForStaffRequirementSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InputsForStaffRequirementSendMail
        fields = "__all__"

class ListInputsForStaffRequirementSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InputsForStaffRequirementSendMail
        fields = "__all__"

# Inputs For Staff Requirement Document
class InputsForStaffRequirementDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InputsForStaffRequirementDocument
        fields = "__all__"

class ListInputsForStaffRequirementDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InputsForStaffRequirementDocument
        fields = "__all__"


class InputsSRSSRSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.InputsSRSSR
        fields = "__all__"


class ListInputsSRSSRSerializer(serializers.ModelSerializer):
    ssr_id= InputsForStaffRequirementSerializer(read_only=True)
    sss = SSSSerializer(read_only=True)
    class Meta: 
        model = models.InputsSRSSR
        fields = "__all__"


# PSR Inputs For Staff Requirement Compartment
class InputsForStaffRequirementCompartmentSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.InputsForStaffRequirementCompartment
        fields = "__all__"

class ListInputsForStaffRequirementCompartmentSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.InputsForStaffRequirementCompartment
        fields = "__all__"


# PSR Inputs For Staff Requirement Equipment
class InputsForStaffRequirementEquipmentSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.InputsForStaffRequirementEquipment
        fields = "__all__"

class ListInputsForStaffRequirementEquipmentSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.InputsForStaffRequirementEquipment
        fields = "__all__"

# PSR Inputs For Staff Requirement System
class InputsForStaffRequirementSystemSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.InputsForStaffRequirementSystem
        fields = "__all__"

class ListInputsForStaffRequirementSystemSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.InputsForStaffRequirementSystem
        fields = "__all__"


# PSR Concept Design
class ConceptDesignSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.ConceptDesign
        fields = "__all__"

class ListConceptDesignSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.ConceptDesign
        fields = "__all__"


# Concept Design Send Mail
class ConceptDesignSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ConceptDesignSendMail
        fields = "__all__"

class ListConceptDesignSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ConceptDesignSendMail
        fields = "__all__"

# Concept Design Document
class ConceptDesignDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ConceptDesignDocument
        fields = "__all__"

class ListConceptDesignDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ConceptDesignDocument
        fields = "__all__"



# PSR Incorporation Of Design Inputs
class IncorporationOfDesignInputsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.IncorporationOfDesignInputs
        fields = "__all__"

class ListIncorporationOfDesignInputsSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.IncorporationOfDesignInputs
        fields = "__all__"

# Incorporation Of Design Inputs Send Mail
class IncorporationOfDesignInputsSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncorporationOfDesignInputsSendMail
        fields = "__all__"

class ListIncorporationOfDesignInputsSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncorporationOfDesignInputsSendMail
        fields = "__all__"

# Incorporation Of Design Inputs Document
class IncorporationOfDesignInputsDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncorporationOfDesignInputsDocument
        fields = "__all__"

class ListIncorporationOfDesignInputsDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncorporationOfDesignInputsDocument
        fields = "__all__"

# PSR Receipt Of RFI Responses
class ReceiptOfRFIResponsesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.ReceiptOfRFIResponses
        fields = "__all__"

class ListReceiptOfRFIResponsesSerializer(serializers.ModelSerializer):

    created_by = Userserializer(read_only=True)
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.ReceiptOfRFIResponses
        fields = "__all__"


class ReceiptOfRFIResponsesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReceiptOfRFIResponsesSendMail
        fields = "__all__"

class ListReceiptOfRFIResponsesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReceiptOfRFIResponsesSendMail
        fields = "__all__"

# Inputs For Staff Requirement Document
class ReceiptOfRFIResponsesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReceiptOfRFIResponsesDocument
        fields = "__all__"

class ListReceiptOfRFIResponsesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReceiptOfRFIResponsesDocument
        fields = "__all__"

# GLS Initiation Notes
class InitiationNotesGLSMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesGLSMaster
        fields = "__all__"       

class ListInitiationNotesGLSSerializer(serializers.ModelSerializer):

    #initiation_notes_gls_master = InitiationNotesGLSMasterSerializer(read_only=True)
    project = projectSerializer(read_only=True)
    created_by = Userserializer(read_only=True)
    document_sections = DocumentSectionsSerializer(read_only=True)
    document_sub_sections = DocumentSubSectionsSerializer(read_only=True)
    document_sub_sections2 = DocumentSubSections2Serializer(read_only=True)
    annexures = AnnexuresSerializer(read_only=True)

    
    class Meta:
        model = models.InitiationNotesGLS
        fields = "__all__" 


class ListInitiationNotesGLSMasterSerializer(serializers.ModelSerializer):

    project = projectSerializer(read_only=True)
    created_by = Userserializer(read_only=True)


    class Meta:
        model = models.InitiationNotesGLSMaster
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        initiation_notes_gls_master=response['id']
        response['details']=ListInitiationNotesGLSSerializer(models.InitiationNotesGLS.objects.filter(initiation_notes_gls_master_id=initiation_notes_gls_master),many=True).data
        return response

class InitiationNotesGLSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesGLS
        fields = "__all__"       

#GLS Initiation Notes upload
class GLSInitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GLSInitiationNotesDocument
        fields = "__all__"

class ListGLSInitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GLSInitiationNotesDocument
        fields = "__all__"

#GLS Initiation Notes Send Mail
class GLSInitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GLSInitiationNotesSendMail
        fields = "__all__"

class ListGLSInitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GLSInitiationNotesSendMail
        fields = "__all__"




# BLS Initiation Notes
class InitiationNotesBLSMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesBLSMaster
        fields = "__all__"       

# class ListInitiationNotesBLSMasterSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.InitiationNotesBLSMaster
#         fields = "__all__" 

class ListInitiationNotesBLSMasterSerializer(serializers.ModelSerializer):
    
    project = projectSerializer(read_only=True)
    created_by = Userserializer(read_only=True)

    class Meta:
        model = models.InitiationNotesBLSMaster
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        initiation_notes_bls_master=response['id']
        response['details']=ListInitiationNotesBLSSerializer(models.InitiationNotesBLS.objects.filter(initiation_notes_bls_master_id=initiation_notes_bls_master),many=True).data
        return response


class InitiationNotesBLSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InitiationNotesBLS
        fields = "__all__"       

class ListInitiationNotesBLSSerializer(serializers.ModelSerializer):

    #initiation_notes_BLS_master = InitiationNotesBLSMasterSerializer(read_only=True)
    project = projectSerializer(read_only=True)
    created_by = Userserializer(read_only=True)
    document_sections = DocumentSectionsSerializer(read_only=True)
    document_sub_sections = DocumentSubSectionsSerializer(read_only=True)
    document_sub_sections2 = DocumentSubSections2Serializer(read_only=True)
    annexures = AnnexuresSerializer(read_only=True)
    
    class Meta:
        model = models.InitiationNotesBLS
        fields = "__all__" 

#BLS Initiation Notes upload
class BLSInitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BLSInitiationNotesDocument
        fields = "__all__"

class ListBLSInitiationNotesDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BLSInitiationNotesDocument
        fields = "__all__"

#BLS Initiation Notes Send Mail
class BLSInitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BLSInitiationNotesSendMail
        fields = "__all__"

class ListBLSInitiationNotesSendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BLSInitiationNotesSendMail
        fields = "__all__"




















######
class ExcelFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExcelFileUpload
        fields = "__all__"       

# class ExcelFileUploadSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.ExcelFileUpload
#         fields = "__all__" 


class ListGlobalStatusSerializer(serializers.ModelSerializer):
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.InitiationNotes
        fields = "__all__" 


class ListGlobalStatusPSRFormulationOfApproachPaperSerializer(serializers.ModelSerializer):
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.FormulationOfApproachPaper
        fields = "__all__" 

class ListGlobalStatusPresentationOfApproachPaperSerializer(serializers.ModelSerializer):
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.PresentationOfApproachPaper
        fields = "__all__" 



class SectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Section
        fields = "__all__"

class UnitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Section
        fields = "__all__"

class CompartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.Compartment
        fields = "__all__"

class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.System
        fields = "__all__"

class EquipementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.Equipment
        fields = "__all__"

class reponsibilitySerializer(serializers.ModelSerializer):
    formulation_of_approach_paper= FormulationOfApproachPaperSerializer(read_only=True)
    project = projectSerializer(read_only=True)

    class Meta:
        model = models.FormulationOfApproachPaperResponsibility
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        formulation_of_approach_paper_responsibility_id=response['id']
        print("response['section']",getArrayValues(response['section']))
        if response['section']:
            response['sections']=SectionsSerializer(models.Section.objects.filter(id__in=getArrayValues(response['section'])),many=True).data
        else:
            response['sections']=[]
        if response['unit']:
            response['units']=SectionsSerializer(models.Section.objects.filter(id__in=getArrayValues(response['unit'])),many=True).data
        else:
            response['units']=[]
        compartments=models.FormulationOfApproachPaperResponsibilityCompartment.objects.values('compartment','id').filter(formulation_of_approach_paper_responsibility_id=formulation_of_approach_paper_responsibility_id).first()
        print("compartments['compartment']",getArrayValues(compartments['compartment']))
        if compartments and compartments['compartment']:
            response['compartments']=CompartmentSerializer(masterModels.Compartment.objects.filter(id__in=getArrayValues(compartments['compartment'])),many=True).data
        else:
            response['compartments']=[]

        systems=models.FormulationOfApproachPaperResponsibilitySystem.objects.values('system','id').filter(formulation_of_approach_paper_responsibility_id=formulation_of_approach_paper_responsibility_id).first()
        if systems and systems['system']:
            response['systems']=SystemSerializer(masterModels.System.objects.filter(id__in=getArrayValues(systems['system'])),many=True).data
        else:
            response['systems']=[]

        equipments=models.FormulationOfApproachPaperResponsibilityEquipment.objects.values('equipment','id').filter(formulation_of_approach_paper_responsibility_id=formulation_of_approach_paper_responsibility_id).first()
        if equipments and equipments['equipment']:
            response['equipments']=EquipementsSerializer(masterModels.Equipment.objects.filter(id__in=getArrayValues(equipments['equipment'])),many=True).data
        else:
            response['equipments']=[]

        return response

class PSRDataFlowCompartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRDataFlowCompartment
        fields = "__all__"

class CompartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.Compartment
        fields = "__all__"

    def to_representation(self, instance):  
        response = super().to_representation(instance)
        compartment_id=response['id']
        project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        data_flow_id=self.context['data_flow_id'] if self.context and 'data_flow_id' in self.context else ""
        response['compartments']=[]
        if data_flow_id:
            response['compartments']=PSRDataFlowCompartmentSerializer(models.PSRDataFlowCompartment.objects.filter(data_flow_id=data_flow_id,compartment_id=compartment_id),many=True).data
        return response

class PSRDataFlowEquipmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRDataFlowEquipments
        fields = "__all__"

class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.Equipment
        fields = "__all__"

    def to_representation(self, instance):  
        response = super().to_representation(instance)
        equipment_id=response['id']
        project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        data_flow_id=self.context['data_flow_id'] if self.context and 'data_flow_id' in self.context else ""
        response['equipments']=[]
        if data_flow_id:
            response['equipments']=PSRDataFlowEquipmentsSerializer(models.PSRDataFlowEquipments.objects.filter(data_flow_id=data_flow_id,equipment_id=equipment_id),many=True).data
        return response

class PSRDataFlowsystemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PSRDataFlowsystems
        fields = "__all__"

class SystemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.System
        fields = "__all__"

    def to_representation(self, instance):  
        response = super().to_representation(instance)
        system_id=response['id']
        project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        data_flow_id=self.context['data_flow_id'] if self.context and 'data_flow_id' in self.context else ""
        response['systems']=[]
        if data_flow_id:
            response['systems']=PSRDataFlowsystemsSerializer(models.PSRDataFlowsystems.objects.filter(data_flow_id=data_flow_id,system_id=system_id),many=True).data
        return response     

class PSRSectionUnitProjectSerializer(serializers.ModelSerializer):
    unit = masterSerializer.UnitSerializer(read_only=True)

    class Meta:
        model = models.PSRSectionUnit
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        section_unit_id=response['id']
        project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        data_flow_id=self.context['data_flow_id'] if self.context and 'data_flow_id' in self.context else ""
        section_id=response['unit']['section_id']
        compartmentsData=masterModels.Compartment.objects.filter(section_id=section_id,status=1)
        equipmentsData=masterModels.Equipment.objects.filter(section_id=section_id,status=1)
        systemsData=masterModels.System.objects.filter(section_id=section_id,status=1)
        print('project_id',project_id)
        if project_id:
            compartmentsData=compartmentsData.filter(id__in=(models.PSRUnitCompartments.objects.values('compartment_id').filter(section_unit_id=section_unit_id,project_id=project_id)))
            equipmentsData=equipmentsData.filter(id__in=(models.PSRUnitEquipments.objects.values('equipment_id').filter(section_unit_id=section_unit_id,project_id=project_id)))
            systemsData=systemsData.filter(id__in=(models.PSRUnitSystems.objects.values('system_id').filter(section_unit_id=section_unit_id,project_id=project_id)))

        response['compartments']=CompartmentSerializer(compartmentsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        response['equipments']=EquipmentSerializer(equipmentsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        response['systems']=SystemSerializer(systemsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        return response

class ResponsibilityPSRSectionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.PSRSection
        fields = "__all__"

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        section_id=response['id']
        response['standards']=''
        response['whole_ship_features']=''
        response['man_power']=''
        response['recommendations']=''
        project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        dataFlow=models.PSRDataFlow.objects.values('id','standards','whole_ship_features','man_power','recommendations').filter(project_id=project_id,psr_section_id=section_id).first()
        if dataFlow:
            response['standards']=dataFlow['standards']
            response['whole_ship_features']=dataFlow['whole_ship_features']
            response['man_power']=dataFlow['man_power']
            response['recommendations']=dataFlow['recommendations']
        response['project_id']=project_id
        data_flow_id=dataFlow['id'] if dataFlow else ''
        response['units']=PSRSectionUnitProjectSerializer(models.PSRSectionUnit.objects.filter(section_id=section_id),many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        return response

class PSRDataFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PSRDataFlow
        fields = "__all__"


class PSRUnitCompartmentsOtherSerializer(serializers.ModelSerializer):
    compartment=masterSerializer.CompartmentSerializer(read_only=True)
    class Meta:
        model = models.PSRUnitCompartments
        fields = "__all__"

class PSRUnitSystemsOtherSerializer(serializers.ModelSerializer):
    system=masterSerializer.SystemSerializer(read_only=True)
    class Meta:
        model = models.PSRUnitSystems
        fields = "__all__"

class PSRUnitEquipmentsOtherSerializer(serializers.ModelSerializer):
    equipment=masterSerializer.EquipmentSerializer(read_only=True)
    class Meta:
        model = models.PSRUnitEquipments
        fields = "__all__"   




class CompletePSRSerializer(serializers.ModelSerializer):
    #unit = masterSerializer.UnitSerializer(read_only=True)

    class Meta:
        model = models.InitiationNotesGLSMaster
        fields = "__all__"   

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        project_id = response['project']
        staff_res = models.InputsForStaffRequirement.objects.values('id','project_id').filter(project_id=project_id)

        sr_id = staff_res[0]['id']

        #lists = models.InitiationNotes.objects.values('approved_status','project__id','project__name').filter(approved_status='2')
        #ssr = models.InputsSRSSR.objects.values('sss__name','description','created_ip').filter(sr_id_id=sr_id).exclude(status='3')


        #lists = models.InputsSRSSR.objects.values('description','sss_id','sss__name').filter(approved_status='2')
        response['sss'] = models.InputsSRSSR.objects.values('description','sss__name','created_ip').filter(sr_id_id=sr_id).exclude(status='3')
        #response['sss'] = InputsSRSSRSerializer(models.InputsSRSSR.objects.values().filter(sr_id_id=sr_id).exclude(status='3'),many=True).data
        #print('project_id',section_unit_id)

        # project_id=self.context['project_id'] if self.context and 'project_id' in self.context else ""
        # data_flow_id=self.context['data_flow_id'] if self.context and 'data_flow_id' in self.context else ""
        # section_id=response['unit']['section_id']
        # compartmentsData=masterModels.Compartment.objects.filter(section_id=section_id,status=1)
        # equipmentsData=masterModels.Equipment.objects.filter(section_id=section_id,status=1)
        # systemsData=masterModels.System.objects.filter(section_id=section_id,status=1)
        # print('project_id',project_id)
        # if project_id:
        #     compartmentsData=compartmentsData.filter(id__in=(models.PSRUnitCompartments.objects.values('compartment_id').filter(section_unit_id=section_unit_id,project_id=project_id)))
        #     equipmentsData=equipmentsData.filter(id__in=(models.PSRUnitEquipments.objects.values('equipment_id').filter(section_unit_id=section_unit_id,project_id=project_id)))
        #     systemsData=systemsData.filter(id__in=(models.PSRUnitSystems.objects.values('system_id').filter(section_unit_id=section_unit_id,project_id=project_id)))

        # response['compartments']=CompartmentSerializer(compartmentsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        # response['equipments']=EquipmentSerializer(equipmentsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        # response['systems']=SystemSerializer(systemsData,many=True,context={"project_id":project_id,"data_flow_id":data_flow_id}).data
        return response


class ProjectModuleMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectModuleMaster
        fields = "__all__"

class ProjectModuleStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectModuleStatus
        fields = "__all__"

class ListProjectModuleStatusSerializer(serializers.ModelSerializer):

    project = projectSerializer(read_only=True)
    project_module_master = ProjectModuleMasterSerializer(read_only=True)

    class Meta:
        model = models.ProjectModuleStatus
        fields = "__all__"



## Gobal Transaction

class GlobalTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalTransaction
        fields = "__all__"

class ListGlobalTransactionSerializer(serializers.ModelSerializer):

    module = masterSerializer.ModuleSerializer(read_only = True)
    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['id']
        response['details'] = ListGlobalTransactionDetailsSerializer(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction),many=True).data
        return response

class GlobalTransactionDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"       

class ListGlobalTransactionDetailsSerializer(serializers.ModelSerializer):

    global_transaction = GlobalTransactionSerializer(read_only=True)
    sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    section = masterSerializer.GlobalSectionSerializer(read_only = True)
    sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__" 


## Global transaction edit

class ListGlobalTransactionEditSerializer(serializers.ModelSerializer):

    #module = masterSerializer.ModuleSerializer(read_only = True)
    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['id']
        #response['details'] = ListGlobalTransactionDetailsEditSerializer2(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction).distinct('sub_module_id'),many=True).data
        #response['details'] = ListGlobalTransactionDetailsEditSerializer2(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction).distinct('section').all(),many=True).data
        #response['section_name'] = masterSerializer.GlobalSectionSerializer(masterModels.GlobalSection.objects.filter(global_transaction_id = global_transaction,sub_section_id = None, sub_sub_section_id = None).exclude(section_id = False),many=True).data)


        response['section'] = ListGlobalTransactionDetailsEditSerializer2(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction,sub_section_id = None, sub_sub_section_id = None).exclude(section_id = False),many=True).data
        return response



class ListGlobalTransactionDetailsEditSerializer2(serializers.ModelSerializer):

    #global_transaction = GlobalTransactionSerializer(read_only=True)
    #sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    #section = masterSerializer.GlobalSectionSerializer(read_only = True)
    # sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    # sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['global_transaction']
        sub_module = response['sub_module']
        section = response['section']

        response['section_name'] = masterSerializer.GlobalSectionSerializer(masterModels.GlobalSection.objects.filter(id = section),many=True).data

        response['sub_section'] = ListGlobalTransactionDetailsEditSerializer3(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction, sub_module_id = sub_module, section_id = section, sub_sub_section_id = None).exclude(sub_section_id = True).order_by('id')[1:],many=True).data
        return response


class ListGlobalTransactionDetailsEditSerializer3(serializers.ModelSerializer):

    #global_transaction = GlobalTransactionSerializer(read_only=True)
    #sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    #section = masterSerializer.GlobalSectionSerializer(read_only = True)
    # sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    # sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['global_transaction']
        sub_module = response['sub_module']
        section = response['section']
        sub_section = response['sub_section']

        response['sub_section_name'] = masterSerializer.GlobalSubSectionSerializer(masterModels.GlobalSubSection.objects.filter(id = sub_section),many=True).data

        response['sub_sub_section'] = ListGlobalTransactionDetailsEditSerializer4(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction, sub_module_id = sub_module, section_id = section, sub_section_id = sub_section).exclude(sub_sub_section_id = None).order_by('id'),many=True).data
        return response

class ListGlobalTransactionDetailsEditSerializer4(serializers.ModelSerializer):

    #global_transaction = GlobalTransactionSerializer(read_only=True)
    #sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    #section = masterSerializer.GlobalSectionSerializer(read_only = True)
    # sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    # sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['global_transaction']
        sub_module = response['sub_module']
        section = response['section']
        sub_section = response['sub_section']
        sub_sub_section = response['sub_sub_section']

        response['sub_sub_section_name'] = masterSerializer.GlobalSubSubSectionSerializer(masterModels.GlobalSubSubSection.objects.filter(id = sub_sub_section),many=True).data

        #response['sub_sub_section'] = ListGlobalTransactionDetailsEditSerializer4(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction, sub_module_id = sub_module, section_id = section, sub_section_id = sub_section).exclude(sub_sub_section_id = None).order_by('id'),many=True).data
        return response



#### Global Transation new


class ListGlobalTransactionAllEditSerializer(serializers.ModelSerializer):

    module = masterSerializer.ModuleSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance) 
        global_transaction = response['id']
        #model = response['module']

        response['sss_mapping'] = SSSMappingSerializer(models.SSSMapping.objects.filter(module_id = 1, status = 1), many=True).data

        response['section'] = ListGlobalSectionSerializer(masterModels.GlobalSection.objects.filter(sub_module_id = 1, status = 1), many=True).data

        response['sub_module'] = masterSerializer.SubModuleSerializer(masterModels.SubModule.objects.filter(id = 1), many=True).data
        return response


#####################################




# class SSSGlobalSectionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = masterModels.GlobalSection
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance) 
#         global_section = response['id']
#         sub_module = response['sub_module']

#         response['section_para'] = SectionParaSerializer_1(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id=None, sub_sub_section_id=None).exclude(status=3), many=True).data

#         response['sub_section'] = GlobalSubSectionSerializer_1(masterModels.GlobalSubSection.objects.filter(global_section_id = global_section, sub_module = sub_module, status = 1),many=True).data
#         return response








#####################################


class ListGlobalSectionSerializer(serializers.ModelSerializer):


    class Meta:
        model = masterModels.GlobalSection
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        #print(response,"GGGGGGGGGRRRRRR")
        global_section = response['id']
        sub_module = response['sub_module']

        response['sub_module'] = masterSerializer.SubModuleSerializer(masterModels.SubModule.objects.filter(id = 1), many=True).data

        response['section_para'] = SectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id=None, sub_sub_section_id=None).exclude(status=3), many=True).data

        response['sub_section'] = GlobalSubSectionSerializer(masterModels.GlobalSubSection.objects.filter(global_section_id = global_section, sub_module = sub_module, status = 1),many=True).data
        return response


class GlobalSubSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.GlobalSubSection
        fields = "__all__"


    def to_representation(self, instance):        
        response = super().to_representation(instance) 

        #print(response,"RRRRRRRRRRR")
        global_section = response['global_section']
        global_sub_section = response['id']
        sub_module = response['sub_module']

        response['sub_section_para'] = SubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id=None).exclude(status=3), many=True).data

        response['sub_sub_section'] = GlobalSubSubSectionSerializer(masterModels.GlobalSubSubSection.objects.filter(global_section_id = global_section, global_sub_section_id = global_sub_section, sub_module_id = sub_module, status = 1),many=True).data
        return response



class GlobalSubSubSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.GlobalSubSubSection
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)

        #print(response,"RRRRRRRRRRR")
        global_section = response['global_section']
        global_sub_section = response['global_sub_section']
        global_sub_sub_section = response['id']
        sub_module = response['sub_module']

        response['sub_sub_section_para'] = SubSubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id = global_sub_sub_section).exclude(status=3), many=True).data

        return response


##############

class SectionParaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"

class SubSectionParaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"

class SubSubSectionParaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"


###### ************ ########
class section(serializers.ModelSerializer):

    class Meta:
        model = masterModels.GlobalSection
        fields = "__all__"


class ListGlobalTransactionAllEditSerializer_1(serializers.ModelSerializer):

    module = masterSerializer.ModuleSerializer(read_only = True)
    project = projectSerializer(read_only=True)
    created_by = Userserializer(read_only=True)

    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        print(response,"Project Id")
        global_transaction = response['id']
        module = response['module']['id']
        #project_id = self.context['project']['id'] 
        #print(response['project']['id'])

        project_id = response['project']['id']
        form = response['form']
        

        response['sss_mapping'] = SSSMappingSerializerNew(models.SSSMapping.objects.filter(module_id = module, status = 1), many=True,context={"project_id":project_id}).data

        #response['sub_module'] = SubModuleSerializer_1(masterModels.SubModule.objects.filter(module_id = module).order_by('id'), context={"project_id":project_id,"module":module}, many=True).data
        return response
         




class SubModuleSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = masterModels.SubModule
        fields = "__all__"

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        print('sdsd',response) 
        project_id = self.context['project_id']
        # global_transaction_id = self.context['global_transaction_id']
        module = self.context['module']
        sub_module = response['id']
        # print('111',self.context['global_transaction_id'])
        # response['section'] = (models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, status = 1).order_by('id'), context={"project_id":project_id}, many=True).data
        response['section'] = (models.GlobalTransactionDetails.objects.values('section__name','sub_module').filter(sub_module_id = response['id']).order_by('id'))
        print('2222',response['section'] )
        return response


class GlobalSectionSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        print(response,"Respone1111")
        project_id = self.context['project_id']
        global_section = response['id']
        # module = self.context['module']
        sub_module = response['sub_module']

        response['section_para'] = SectionParaSerializer_1(models.GlobalTransactionDetails.objects.filter( section_id = global_section, sub_section_id=None, sub_sub_section_id=None, project_id = project_id).exclude(status=3), many=True).data

        # response['sub_section'] = GlobalSubSectionSerializer_1(masterModels.GlobalSubSection.objects.filter(global_section_id = global_section, module_id = module, status = 1).order_by('id'), context={"project_id":project_id,"module":module}, many=True).data
        return response


class SectionParaSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"


# class GlobalSubSectionSerializer_1(serializers.ModelSerializer):
    
#     class Meta:
#         model = masterModels.GlobalSubSection
#         fields = "__all__"


class GlobalSubSectionSerializer_1(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.GlobalSubSection
        fields = "__all__"


    def to_representation(self, instance):        
        response = super().to_representation(instance)

        project_id = self.context['project_id']
        global_section = response['global_section']
        global_sub_section = response['id']
        sub_module = response['sub_module']
        module = self.context['module']

        response['sub_section_para'] = SubSectionParaSerializer_1(models.GlobalTransactionDetails.objects.filter( section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id=None, project_id = project_id).exclude(status=3), many=True).data

        response['sub_sub_section'] = GlobalSubSubSectionSerializer_1(masterModels.GlobalSubSubSection.objects.filter(global_section_id = global_section, global_sub_section_id = global_sub_section, module_id = module, status = 1).order_by('id'), context={"project_id":project_id}, many=True).data
        return response


class SubSectionParaSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"


class GlobalSubSubSectionSerializer_1(serializers.ModelSerializer):
    
    class Meta:
        model = masterModels.GlobalSubSubSection
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        project_id = self.context['project_id']
        global_section = response['global_section']
        global_sub_section = response['global_sub_section']
        global_sub_sub_section = response['id']
        sub_module = response['sub_module']

        response['sub_sub_section_para'] = SubSubSectionParaSerializer_1(models.GlobalTransactionDetails.objects.filter( section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id = global_sub_sub_section, project_id = project_id).exclude(status=3), many=True).data

        return response

class SubSubSectionParaSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"



#################

class SSSMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SSSMapping
        fields = "__all__"       

class ListSSSMappingSerializer(serializers.ModelSerializer):
    
    module = masterSerializer.ModuleSerializer(read_only = True)
    sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    section = masterSerializer.GlobalSectionSerializer(read_only = True)
    sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)
    
    class Meta:
        model = models.SSSMapping
        fields = "__all__" 


###### SSS Mapping #######

class SSSMappingSerializerNew(serializers.ModelSerializer):


    #section = masterSerializer.GlobalSectionSerializer(read_only = True)
    class Meta:
        model = models.SSSMapping
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        project_id=self.context['project_id'] if 'project_id' in self.context else '' 
        #print(response, "SSS")
        module = response['module']
        sub_module = response['sub_module']

        global_section = response['section']
        global_sub_section = response['sub_section']
        global_sub_sub_section = response['sub_sub_section']

        response['section'] = SSSGlobalSectionSerializer(masterModels.GlobalSection.objects.filter(sub_module_id = sub_module, id = global_section, status = 1), many=True,context={"project_id":project_id}).data

        response['sub_section'] = SSSGlobalSubSectionSerializer(masterModels.GlobalSubSection.objects.filter(sub_module_id = sub_module, id = global_sub_section, global_section_id = global_section, status = 1), many=True,context={"project_id":project_id}).data

        response['sub_sub_section'] = SSSGlobalSubSubSectionSerializer(masterModels.GlobalSubSubSection.objects.filter(sub_module_id = sub_module, id = global_sub_sub_section, global_section_id = global_section,  global_sub_section_id = global_sub_section, status = 1), many=True,context={"project_id":project_id}).data

        return response


class SSSGlobalSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.GlobalSection
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        global_section = response['id']
        sub_module = response['sub_module']
        project_id=self.context['project_id'] if 'project_id' in self.context else None

        response['section_para'] = SSSMappingParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id=None, sub_sub_section_id=None,project_id=project_id).exclude(status=3), many=True).data
        return response




class SSSGlobalSubSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.GlobalSubSection
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        global_section = response['global_section']
        global_sub_section = response['id']
        sub_module = response['sub_module']
        project_id=self.context['project_id'] if 'project_id' in self.context else None
        response['sub_section_para'] = SSSMappingParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id=None,project_id=project_id).exclude(status=3), many=True).data

        return response


class SSSGlobalSubSubSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = masterModels.GlobalSubSubSection
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        global_section = response['global_section']
        global_sub_section = response['global_sub_section']
        global_sub_sub_section = response['id']
        sub_module = response['sub_module']
        project_id=self.context['project_id'] if 'project_id' in self.context else None
        response['sub_sub_section_para'] = SSSMappingParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id = global_sub_sub_section,project_id=project_id).exclude(status=3), many=True).data

        return response


class SSSMappingParaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalTransactionDetails
        fields = "__all__"

#######################33
class ListGlobalStatusSerializer1(serializers.ModelSerializer):
    project = projectSerializer(read_only=True)
    
    class Meta:
        model = models.GlobalTransaction
        fields = "__all__"         


##### Forms and Forms Mapping ######

class FormsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Forms
        fields = "__all__"


class ListFormsMappingSerializer(serializers.ModelSerializer):
    Class = masterSerializer.ClassSerializer(read_only = True)
    module = masterSerializer.ModuleSerializer(read_only = True)
    sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    section = masterSerializer.GlobalSectionSerializer(read_only = True)
    sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)

    class Meta:
        model = models.FormsMapping
        fields = "__all__"

class ListFormsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Forms
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        form_id=response['id']
        response['form_mapping']=ListFormsMappingSerializer(models.FormsMapping.objects.filter(form_id=form_id),many=True).data
        return response

class ListFormsWOTMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Forms
        fields = ("id","name","code","status")


class FormsMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

 

class FormsLevelRecommenderHierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FormLevelRecommenderHierarchy
        fields = "__all__"


class FormsLevelApproverHierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FormLevelApproverHierarchy
        fields = "__all__"


class ProjectLevelRecommenderHierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ProjectLevelRecommenderHierarchy
        fields = "__all__"

class ProjectLevelApproverHierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ProjectLevelApproverHierarchy
        fields = "__all__"


#### Template Generation ####

class TemplateGenerateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        form = response['form']
        module = response['module']
        sub_module = response['sub_module']
        section = response['section']
        sub_section = response['sub_section']
        sub_sub_section = response['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['form'] = ListFormsSerializer2(models.Forms.objects.filter(id = 1, status = 1).order_by('id'), many = True, context = context).data
        return response



class ListFormsSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.Forms
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        form = self.context['form']
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['module'] = ListModuleSerializer2(masterModels.Module.objects.filter(id = module, status = 1).order_by('id'), many = True, context = context).data
        return response


class ListModuleSerializer2(serializers.ModelSerializer):

    class Meta:
        model = masterModels.Module
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        form = self.context['form']
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['sub_module'] = ListSubModuleSerializer2(masterModels.SubModule.objects.filter(id = sub_module, module = module, status = 1).order_by('id'), many = True, context = context).data
        return response


class ListSubModuleSerializer2(serializers.ModelSerializer):

    class Meta:
        model = masterModels.SubModule
        fields = "__all__"


    def to_representation(self, instance):
        response = super().to_representation(instance)

        form = self.context['form']
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['section'] = ListFormsMappingSerializer3(models.FormsMapping.objects.filter(section = section, status = 1), many = True, context = context).data
        return response


# class ListFormsMappingSerializer2(serializers.ModelSerializer):

#     class Meta:
#         model = models.FormsMapping
#         fields = "__all__"


#     def to_representation(self, instance):
#         response = super().to_representation(instance)

#         form = self.context['form']
#         module = self.context['module']
#         sub_module = self.context['sub_module']
#         section = self.context['section']
#         sub_section = self.context['sub_section']
#         sub_sub_section = self.context['sub_sub_section']

#         context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

#         response['section'] = ListGlobalSectionSerializer2(models.GlobalSection.objects.filter(id = section, status = 1).order_by('id'), many = True, context = context).data
#         return response












class ListFormsMappingSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.FormsMapping
        fields = "__all__"


    def to_representation(self, instance):
        response = super().to_representation(instance)

        form = self.context['form']
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['section1'] = ListFormsMappingSerializer3(models.FormsMapping.objects.filter(section = section, sub_section = sub_section, status = 1).order_by('id'), many = True, context = context).data
        return response



class ListFormsMappingSerializer3(serializers.ModelSerializer):

    class Meta:
        model = models.FormsMapping
        fields = "__all__"


    def to_representation(self, instance):
        response = super().to_representation(instance)

        form = self.context['form']
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        context = {"form":form, "module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['section'] = ListGlobalSectionSerializer2(models.GlobalSection.objects.filter(id = section, status = 1).order_by('id'), many = True, context = context).data
        return response


class ListGlobalSectionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalSection
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']

        global_section = response['id']
        # module = response['module']
        # sub_module = response['sub_module']

        context = {"module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['section_para'] = SectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = None, sub_sub_section = None).exclude(status=3), many=True).data

        response['sub_section'] = ListGlobalSubSectionSerializer2(models.GlobalSubSection.objects.filter(id = sub_section, module = module, sub_module = sub_module, status = 1), many=True, context = context).data
        return response


class ListGlobalSubSectionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalSubSection
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)

        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']
        
        global_sub_section = response['id']
        # global_section = response['global_section']
        # module = response['module']
        # sub_module = response['sub_module']

        context = {"module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

        response['sub_section_para'] = SubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = sub_section, sub_sub_section = None).exclude(status=3), many=True).data

        response['sub_sub_section'] = ListGlobalSubSubSectionSerializer2(models.GlobalSubSubSection.objects.filter(id = sub_sub_section, module = module, sub_module = sub_module, status = 1), many=True, context = context).data

        # response['sub_sub_section_para'] = SubSubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id = global_sub_sub_section).exclude(status=3), many=True).data
        return response


class ListGlobalSubSubSectionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalSubSubSection
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)

        module = self.context['module']
        sub_module = self.context['sub_module']
        section = self.context['section']
        sub_section = self.context['sub_section']
        sub_sub_section = self.context['sub_sub_section']
        
        global_sub_section = response['id']
        # global_section = response['global_section']
        # module = response['module']
        # sub_module = response['sub_module']

        response['sub_sub_section_para'] = SubSubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = sub_section, sub_sub_section = sub_sub_section).exclude(status=3), many=True).data  











#### Template Generation ####

# class TemplateGenerateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.FormsMapping
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance) 
#         form = response['id']
#         module = response['module']
#         sub_module = response['sub_module']
#         section = response['section']
#         sub_section = response['sub_section']
#         sub_sub_section = response['sub_sub_section']

#         context = {"module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

#         response['section'] = ListGlobalSectionSerializer2(models.GlobalSection.objects.filter(id = section, module = module, sub_module = sub_module, status = 1).order_by('id'), many = True, context = context).data
#         return response


# class ListGlobalSectionSerializer2(serializers.ModelSerializer):

#     class Meta:
#         model = models.GlobalSection
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
        
#         module = self.context['module']
#         sub_module = self.context['sub_module']
#         section = self.context['section']
#         sub_section = self.context['sub_section']
#         sub_sub_section = self.context['sub_sub_section']

#         global_section = response['id']
#         # module = response['module']
#         # sub_module = response['sub_module']

#         context = {"module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

#         response['section_para'] = SectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = None, sub_sub_section = None).exclude(status=3), many=True).data

#         response['sub_section'] = ListGlobalSubSectionSerializer2(models.GlobalSubSection.objects.filter(id = sub_section, module = module, sub_module = sub_module, status = 1), many=True, context = context).data
#         return response


# class ListGlobalSubSectionSerializer2(serializers.ModelSerializer):

#     class Meta:
#         model = models.GlobalSubSection
#         fields = "__all__" 

#     def to_representation(self, instance):
#         response = super().to_representation(instance)

#         module = self.context['module']
#         sub_module = self.context['sub_module']
#         section = self.context['section']
#         sub_section = self.context['sub_section']
#         sub_sub_section = self.context['sub_sub_section']
        
#         global_sub_section = response['id']
#         # global_section = response['global_section']
#         # module = response['module']
#         # sub_module = response['sub_module']

#         context = {"module":module, "sub_module":sub_module, "section":section, "sub_section":sub_section, "sub_sub_section":sub_sub_section}

#         response['sub_section_para'] = SubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = sub_section, sub_sub_section = None).exclude(status=3), many=True).data

#         response['sub_sub_section'] = ListGlobalSubSubSectionSerializer2(models.GlobalSubSubSection.objects.filter(id = sub_sub_section, module = module, sub_module = sub_module, status = 1), many=True, context = context).data

#         # response['sub_sub_section_para'] = SubSubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module_id = sub_module, section_id = global_section, sub_section_id= global_sub_section, sub_sub_section_id = global_sub_sub_section).exclude(status=3), many=True).data
#         return response


# class ListGlobalSubSubSectionSerializer2(serializers.ModelSerializer):

#     class Meta:
#         model = models.GlobalSubSubSection
#         fields = "__all__" 

#     def to_representation(self, instance):
#         response = super().to_representation(instance)

#         module = self.context['module']
#         sub_module = self.context['sub_module']
#         section = self.context['section']
#         sub_section = self.context['sub_section']
#         sub_sub_section = self.context['sub_sub_section']
        
#         global_sub_section = response['id']
#         # global_section = response['global_section']
#         # module = response['module']
#         # sub_module = response['sub_module']

#         response['sub_sub_section_para'] = SubSubSectionParaSerializer(models.GlobalTransactionDetails.objects.filter(sub_module = sub_module, section = section, sub_section = sub_section, sub_sub_section = sub_sub_section).exclude(status=3), many=True).data  



# class ListGlobalTransactionSerializer(serializers.ModelSerializer):

#     module = masterSerializer.ModuleSerializer(read_only = True)
#     class Meta:
#         model = models.GlobalTransaction
#         fields = "__all__" 

class getFormMappingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        section_view=True
        section_paragraph=''
        section_paragraphlog=''
        # section_paragraphlog=''
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet
        sectionSet=models.FormsMapping.objects.values('section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id).distinct('section_id')

        newReponse['section']=[]
        responseSections=[]
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                 
                sParaNolog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).first()

                sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                #print(section_para_no)
                section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''
                section_para_nolog=sParaNolog['para_no'] if sParaNolog is not None and sParaNolog['para_no'] is not None else ''
                #print(section_para_nolog, "SSSSSSssss")
                
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True
               

                
                
                    
                    
            subsectionSet=models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id).distinct('sub_section__id')
            subsections=[]
            
            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_paragraphlog=''
                sub_section_view=True
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()

                    sParaNolog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()

                    sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''

                    sub_section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''
                    sub_section_para_nolog=sParaNolog['para_no'] if sParaNolog is not None and sParaNolog['para_no'] is not None else ''

                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')
                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_paragraphlog=''
                    sub_sub_section_view=True
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()

                        sParaNolog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()

                        sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''

                        sub_sub_section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''

                        sub_sub_section_para_nolog=sParaNolog['para_no'] if sParaNolog is not None and sParaNolog['para_no'] is not None else ''

                        #print(sub_sub_section_para_nolog,"GGGHHKK12121")

                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'para_no':sub_sub_section_para_no,'paragraphlog':sub_sub_section_paragraphlog,'para_nolog':sub_sub_section_para_nolog,'view':sub_sub_section_view})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'para_no':sub_section_para_no,'paragraphlog':sub_section_paragraphlog,'para_nolog':sub_section_para_nolog,'sub_module':subModuleDet['id'],'subsubsections':subsubsections,'view':sub_section_view})

            responseSections.append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph,'para_no':section_para_no,'paragraphlog':section_paragraphlog,'para_nolog':section_para_nolog,'subsections':subsections,'view':section_view})

        newReponse['submodule']['section']=responseSections
        return newReponse


class getFormMappingSystemEquipementCompartmentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        section_view=True
        section_paragraph=''
        section_para_no=''
        section_paragraphlog=''
        # section_paragraphlog=''
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet
        sectionSet=models.FormsMapping.objects.values('section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id).distinct('section_id')

        newReponse['section']=[]
        responseSections=[]
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                 
                sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''
                
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True
               
                ## System ##
                sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_system = sSystem

                sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=1)
                section_system_value = sSystemValue
                

                ## Equipment ##
                sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_equipment = sEquipment

                sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=2)
                section_equipment_value = sEquipmentValue

                ## Compartment ##
                sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_compartment = sCompartment

                sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=3)
                section_compartment_value = sCompartmentValue               
                
                    
                    
            subsectionSet=models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id).distinct('sub_section__id')
            subsections=[]
            
            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_paragraphlog=''
                sub_section_view=True
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    
                    sView=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    
                    sub_section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''
                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True


                    ## System ##
                    sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_system = sSystem

                    sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=1)
                    sub_section_system_value = sSystemValue
                    # print(sub_section_system_value,"8888")
                    #arr_name = 
                    #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                    ## Equipment ##
                    sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_equipment = sEquipment

                    sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=2)
                    sub_section_equipment_value = sEquipmentValue

                    ## Compartment ##
                    sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_compartment = sCompartment

                    sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id, sub_section_id=subsection['sub_section__id'], sub_sub_section_id__isnull=True, type=3)
                    sub_section_compartment_value = sCompartmentValue



                subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')
                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_paragraphlog=''
                    sub_sub_section_view=True
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sParalog=models.GlobalTransactionDetailsLog.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sView=models.GlobalTransactionDetails.objects.values('paragraph','view').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_sub_section_paragraphlog=sParalog['paragraph'] if sParalog is not None and sParalog['paragraph'] is not None else ''
                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True

                        ## System ##
                        sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_system = sSystem

                        sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=1)
                        sub_sub_section_system_value = sSystemValue


                        #arr_name = 
                        #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                        ## Equipment ##
                        sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_equipment = sEquipment

                        sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=2)
                        sub_sub_section_equipment_value = sEquipmentValue

                        ## Compartment ##
                        sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_compartment = sCompartment

                        sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=3)
                        sub_sub_section_compartment_value = sCompartmentValue



                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'paragraphlog':sub_sub_section_paragraphlog,'view':sub_sub_section_view, 'system':sub_sub_section_system,'system_value':sub_sub_section_system_value, 'equipment':sub_sub_section_equipment, 'equipment_value':sub_sub_section_equipment_value, 'compartment':sub_sub_section_compartment,'compartment_value':sub_sub_section_compartment_value})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'paragraphlog':sub_section_paragraphlog,'sub_module':subModuleDet['id'],'subsubsections':subsubsections,'view':sub_section_view, 'system':sub_section_system, 'system_value':sub_section_system_value, 'equipment':sub_section_equipment, 'equipment_value':sub_section_equipment_value, 'compartment':sub_section_compartment, 'compartment_value':sub_section_compartment_value})

            responseSections.append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph, 'para_no':'007', 'paragraphlog':section_paragraphlog,'subsections':subsections,'view':section_view,'system':section_system, 'system_value':section_system_value, 'equipment':section_equipment, 'equipment_value':section_equipment_value,'compartment':section_compartment,'compartment_value':section_compartment_value})
        newReponse['submodule']['section']=responseSections
        print(newReponse)
        return newReponse



class getVersionFormMappingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        section_view=True
        section_paragraph=''
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet
        sectionSet=models.FormsMapping.objects.values('section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id).distinct('section_id')

        #print(self.context['version_id'],"FFFFFF")

        newReponse['section']=[]
        responseSections=[]
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, version_id=self.context['version_id']).exclude(paragraph='').first()
                sView=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, version_id=self.context['version_id']).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True
        
        
            subsectionSet=models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id).distinct('sub_section__id')
            subsections=[]
            
            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_view=True
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, version_id=self.context['version_id']).exclude(paragraph='').first()
                    sView=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, version_id=self.context['version_id']).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')
                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_view=True
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], version_id=self.context['version_id']).exclude(paragraph='').first()
                        sView=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], version_id=self.context['version_id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'view':sub_sub_section_view})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'sub_module':subModuleDet['id'],'subsubsections':subsubsections,'view':sub_section_view})
            responseSections.append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph,'subsections':subsections,'view':section_view})
        newReponse['submodule']['section']=responseSections
        return newReponse

class getFormMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        
        newReponse['project']=self.context['project_id']
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet

        #OLD
        #sectionSet=models.FormsMapping.objects.values('id','order','sub_module_id','section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id,form_id=form_id).distinct('section_id')

        sectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_module_id','section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id,form_id=form_id).distinct('section_id').exclude(order=None)
        #print(sectionSet_Ids.query,"HHHH")

        section_ids = [d['id'] for d in sectionSet_Ids]
        sectionSet=models.FormsMapping.objects.filter(id__in=section_ids).values('id','order','sub_module_id','section__id','section__name','section__code').order_by('order')

        #print(sectionSet.query,"FFFFF")
        newReponse['section']=[]
        section_view=True
        section_paragraph=''
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                sView=models.GlobalTransactionDetails.objects.values('view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull       =True).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True

                sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id__isnull=True,sub_sub_section_id__isnull=True)
                section_comments = sComments

                if self.context['directorate_id']!="":
                    sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, directorate_id=self.context['directorate_id']).first()
                    section_directorate = sDirectorate
                else:
                    section_directorate = ''


                sFieldType = masterModels.GlobalSection.objects.values("data_type","default_values").filter(id=section_id,module_id=module_id,sub_module_id=sub_module_id).first()
                section_field_type = sFieldType


                ## System ##
                sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_system = sSystem

                sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=1)
                section_system_value = sSystemValue

                ## Equipment ##
                sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_equipment = sEquipment

                sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=2)
                section_equipment_value = sEquipmentValue

                ## Compartment ##
                sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_compartment = sCompartment

                sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=3)
                section_compartment_value = sCompartmentValue

            # OLD
            #subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')

            subsectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False,form_id=form_id).distinct('sub_section__id').exclude(order=None)
            #print(subsectionSet_Ids.query,"AAAAAA")

            subsection_ids = [d['id'] for d in subsectionSet_Ids]

            if not subsection_ids:
                subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')
            else:
                subsectionSet = models.FormsMapping.objects.filter(id__in=subsection_ids).values('id','order','sub_section__id','sub_section__name','sub_section__code').order_by('id')
                #print(subsectionSet.query,"BBBBB")

            subsections=[]

            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_view=True
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''

                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True


                    sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True)
                    sub_section_comments = sComments
                    
                    if self.context['directorate_id']!="":
                        sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True,directorate_id=self.context['directorate_id']).first()
                        sub_section_directorate = sDirectorate
                    else:
                        sub_section_directorate=''

                    sFieldType = masterModels.GlobalSubSection.objects.values("data_type","default_values").filter(id=subsection['sub_section__id'], module_id=module_id, sub_module_id=sub_module_id).first()
                    sub_section_field_type = sFieldType


                    ## System ##
                    sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_system = sSystem

                    sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=1)
                    sub_section_system_value = sSystemValue

                    #arr_name = 
                    #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                    ## Equipment ##
                    sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_equipment = sEquipment

                    sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=2)
                    sub_section_equipment_value = sEquipmentValue

                    ## Compartment ##
                    sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_compartment = sCompartment

                    sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id, sub_section_id=subsection['sub_section__id'], sub_sub_section_id__isnull=True, type=3)
                    sub_section_compartment_value = sCompartmentValue

                #OLD
                #subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')

                subsubsectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id'],form_id=form_id).distinct('sub_sub_section__id').exclude(order=None)

                subsubsection_ids = [d['id'] for d in subsubsectionSet_Ids]

                # if not subsection_ids:
                #     subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')
                # else:
                #     subsectionSet = models.FormsMapping.objects.filter(id__in=subsection_ids).values('id','order','sub_section__id','sub_section__name','sub_section__code').order_by('id')

                subsubsectionSet = models.FormsMapping.objects.filter(id__in=subsubsection_ids).values('id','order','sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').order_by('id')

                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_view=''
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True


                        sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_comments = sComments

                        if self.context['directorate_id']!="":
                            sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'],directorate_id=self.context['directorate_id']).first()
                            sub_sub_section_directorate = sDirectorate
                        else:
                            sub_sub_section_directorate=''

                        sFieldType = masterModels.GlobalSubSubSection.objects.values("data_type","default_values").filter(id=subsubsection['sub_sub_section__id'], module_id=module_id, sub_module_id=sub_module_id).first()
                        sub_sub_section_field_type = sFieldType

                        ## System ##
                        sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_system = sSystem

                        sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=1)
                        sub_sub_section_system_value = sSystemValue


                        #arr_name = 
                        #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                        ## Equipment ##
                        sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_equipment = sEquipment

                        sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=2)
                        sub_sub_section_equipment_value = sEquipmentValue

                        ## Compartment ##
                        sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_compartment = sCompartment

                        sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=3)
                        sub_sub_section_compartment_value = sCompartmentValue


                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'para_no':sub_section_para_no,'view':sub_sub_section_view,'comments':sub_sub_section_comments, 'directorate':sub_sub_section_directorate, 'field_type':sub_sub_section_field_type, 'system':sub_sub_section_system,'system_value':sub_sub_section_system_value, 'equipment':sub_sub_section_equipment, 'equipment_value':sub_sub_section_equipment_value, 'compartment':sub_sub_section_compartment,'compartment_value':sub_sub_section_compartment_value})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'para_no':sub_section_para_no,'view':sub_section_view,'sub_module':subModuleDet['id'],'subsubsections':subsubsections, 'comments':sub_section_comments, 'directorate':sub_section_directorate, 'field_type':sub_section_field_type, 'system':sub_section_system, 'system_value':sub_section_system_value, 'equipment':sub_section_equipment, 'equipment_value':sub_section_equipment_value, 'compartment':sub_section_compartment, 'compartment_value':sub_section_compartment_value})
            newReponse['section'].append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph,'para_no':section_para_no,'view':section_view,'subsections':subsections,'comments':section_comments, 'directorate':section_directorate, 'field_type':section_field_type, 'system':section_system, 'system_value':section_system_value, 'equipment':section_equipment, 'equipment_value':section_equipment_value,'compartment':section_compartment,'compartment_value':section_compartment_value})

        return newReponse


class getFormMappingSerializerVersion(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        
        newReponse['project']=self.context['project_id']
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet

        #OLD
        #sectionSet=models.FormsMapping.objects.values('id','order','sub_module_id','section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id,form_id=form_id).distinct('section_id')

        sectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_module_id','section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id,form_id=form_id).distinct('section_id').exclude(order=None)
        #print(sectionSet_Ids.query,"HHHH")

        section_ids = [d['id'] for d in sectionSet_Ids]
        sectionSet=models.FormsMapping.objects.filter(id__in=section_ids).values('id','order','sub_module_id','section__id','section__name','section__code').order_by('order')

        #print(sectionSet.query,"FFFFF")
        newReponse['section']=[]
        section_view=True
        section_paragraph=''
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                sView=models.GlobalTransactionDetails.objects.values('view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull       =True).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True

                sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id__isnull=True,sub_sub_section_id__isnull=True)
                section_comments = sComments

                # if self.context['directorate_id']!="":
                #     sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, directorate_id=self.context['directorate_id']).first()
                #     section_directorate = sDirectorate
                # else:
                #     section_directorate = ''

                section_directorate = ''

                sFieldType = masterModels.GlobalSection.objects.values("data_type","default_values").filter(id=section_id,module_id=module_id,sub_module_id=sub_module_id).first()
                section_field_type = sFieldType


                ## System ##
                sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_system = sSystem

                sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=1)
                section_system_value = sSystemValue

                ## Equipment ##
                sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_equipment = sEquipment

                sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=2)
                section_equipment_value = sEquipmentValue

                ## Compartment ##
                sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True)
                section_compartment = sCompartment

                sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True, type=3)
                section_compartment_value = sCompartmentValue

            # OLD
            #subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')

            subsectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False,form_id=form_id).distinct('sub_section__id').exclude(order=None)
            #print(subsectionSet_Ids.query,"AAAAAA")

            subsection_ids = [d['id'] for d in subsectionSet_Ids]

            if not subsection_ids:
                subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')
            else:
                subsectionSet = models.FormsMapping.objects.filter(id__in=subsection_ids).values('id','order','sub_section__id','sub_section__name','sub_section__code').order_by('id')
                #print(subsectionSet.query,"BBBBB")

            subsections=[]

            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_view=True
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''

                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True


                    sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True)
                    sub_section_comments = sComments
                    
                    # if self.context['directorate_id']!="":
                    #     sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True,directorate_id=self.context['directorate_id']).first()
                    #     sub_section_directorate = sDirectorate
                    # else:
                    #     sub_section_directorate=''

                    sub_section_directorate=''

                    sFieldType = masterModels.GlobalSubSection.objects.values("data_type","default_values").filter(id=subsection['sub_section__id'], module_id=module_id, sub_module_id=sub_module_id).first()
                    sub_section_field_type = sFieldType


                    ## System ##
                    sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_system = sSystem

                    sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=1)
                    sub_section_system_value = sSystemValue

                    #arr_name = 
                    #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                    ## Equipment ##
                    sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_equipment = sEquipment

                    sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True, type=2)
                    sub_section_equipment_value = sEquipmentValue

                    ## Compartment ##
                    sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id__isnull=True)
                    sub_section_compartment = sCompartment

                    sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id, sub_section_id=subsection['sub_section__id'], sub_sub_section_id__isnull=True, type=3)
                    sub_section_compartment_value = sCompartmentValue

                #OLD
                #subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')

                subsubsectionSet_Ids=models.FormsMapping.objects.values('id','order','sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id'],form_id=form_id).distinct('sub_sub_section__id').exclude(order=None)

                subsubsection_ids = [d['id'] for d in subsubsectionSet_Ids]

                # if not subsection_ids:
                #     subsectionSet = models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id__isnull=False).distinct('sub_section__id')
                # else:
                #     subsectionSet = models.FormsMapping.objects.filter(id__in=subsection_ids).values('id','order','sub_section__id','sub_section__name','sub_section__code').order_by('id')

                subsubsectionSet = models.FormsMapping.objects.filter(id__in=subsubsection_ids).values('id','order','sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').order_by('id')

                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_view=''
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sView=models.GlobalTransactionDetails.objects.values('paragraph','view','para_no').filter(global_transaction__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_section_para_no=sView['para_no'] if sView is not None and sView['para_no'] is not None else ''
                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True


                        sComments=models.GlobalTransactionComments.objects.values("id","comments","created_on","created_by__first_name","created_by__last_name","created_by__id","project","module","sub_module","section","sub_section","sub_sub_section").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id, sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_comments = sComments

                        # if self.context['directorate_id']!="":
                        #     sDirectorate=models.GlobalTransactionResponsibilityDetail.objects.values("id","directorate_id","directorate_id__code").filter(module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'],directorate_id=self.context['directorate_id']).first()
                        #     sub_sub_section_directorate = sDirectorate
                        # else:
                        #     sub_sub_section_directorate=''

                        sub_sub_section_directorate=''

                        sFieldType = masterModels.GlobalSubSubSection.objects.values("data_type","default_values").filter(id=subsubsection['sub_sub_section__id'], module_id=module_id, sub_module_id=sub_module_id).first()
                        sub_sub_section_field_type = sFieldType

                        ## System ##
                        sSystem = models.System.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_system = sSystem

                        sSystemValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=1)
                        sub_sub_section_system_value = sSystemValue


                        #arr_name = 
                        #sSystemJson = "[{'ser':'1','name':'kalam','numbers':'123','capabilities_feature':'','weight_volume_power_consumption':'','location':'','interface':'','procurement_router':'','vendor':'','cost':'','standards':'','sustenance':''}]"

                        ## Equipment ##
                        sEquipment = models.Equipment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_equipment = sEquipment

                        sEquipmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id','ser','name','numbers', 'capabilities_feature', 'weight_volume_power_consumption', 'location', 'interface', 'procurement_router', 'vendor', 'cost', 'standards', 'sustenance').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=2)
                        sub_sub_section_equipment_value = sEquipmentValue

                        ## Compartment ##
                        sCompartment = models.Compartment.objects.values('name','global_section_id','global_sub_section_id', 'global_sub_sub_section_id').filter(global_section_id=section_id,global_sub_section_id=subsection['sub_section__id'],global_sub_sub_section_id=subsubsection['sub_sub_section__id'])
                        sub_sub_section_compartment = sCompartment

                        sCompartmentValue = models.SystemEquipmentCompartment.objects.values('section_id','sub_section_id','sub_sub_section_id', 'type', 'ser','name','numbers', 'location', 'equipment', 'features', 'layout', 'special_requirements', 'standards').filter(project_id=self.context['project_id'], section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id'], type=3)
                        sub_sub_section_compartment_value = sCompartmentValue


                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'para_no':sub_section_para_no,'view':sub_sub_section_view,'comments':sub_sub_section_comments, 'directorate':sub_sub_section_directorate, 'field_type':sub_sub_section_field_type, 'system':sub_sub_section_system,'system_value':sub_sub_section_system_value, 'equipment':sub_sub_section_equipment, 'equipment_value':sub_sub_section_equipment_value, 'compartment':sub_sub_section_compartment,'compartment_value':sub_sub_section_compartment_value})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'para_no':sub_section_para_no,'view':sub_section_view,'sub_module':subModuleDet['id'],'subsubsections':subsubsections, 'comments':sub_section_comments, 'directorate':sub_section_directorate, 'field_type':sub_section_field_type, 'system':sub_section_system, 'system_value':sub_section_system_value, 'equipment':sub_section_equipment, 'equipment_value':sub_section_equipment_value, 'compartment':sub_section_compartment, 'compartment_value':sub_section_compartment_value})
            newReponse['section'].append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph,'para_no':section_para_no,'view':section_view,'subsections':subsections,'comments':section_comments, 'directorate':section_directorate, 'field_type':section_field_type, 'system':section_system, 'system_value':section_system_value, 'equipment':section_equipment, 'equipment_value':section_equipment_value,'compartment':section_compartment,'compartment_value':section_compartment_value})

        return newReponse


class getVersionMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        newReponse={}
        form_id=response['form']
        module_id=response['module']
        sub_module_id=response['sub_module']
        section_id=response['section']
        sub_section_id=response['sub_section']
        sub_sub_section_id=response['sub_sub_section']
        
        ModuleDet=masterModels.Module.objects.values('id','name').filter(id=module_id).first()
        newReponse['module']=ModuleDet
        subModuleDet=masterModels.SubModule.objects.values('id','name').filter(id=sub_module_id).first()
        newReponse['submodule']=subModuleDet
        sectionSet=models.FormsMapping.objects.values('section__id','section__name','section__code').filter(module_id=module_id,sub_module_id=sub_module_id).distinct('section_id')

        newReponse['section']=[]
        section_view=True
        section_paragraph=''
        for section in sectionSet:
            section_id=section['section__id']

            if 'project_id' in self.context and self.context['project_id']!='':
                sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                sView=models.VersionTransaction.objects.values('view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id__isnull=True,sub_sub_section_id__isnull=True).first()
                section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                section_view=sView['view'] if sView is not None and sView['view'] is not None else True

        
        
            subsectionSet=models.FormsMapping.objects.values('sub_section__id','sub_section__name','sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id).distinct('sub_section__id')
            subsections=[]
            
            for subsection in subsectionSet:
                sub_section_paragraph=''
                sub_section_view=True 
                subsubsections=[]
                if 'project_id' in self.context and self.context['project_id']!='':
                    sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).exclude(paragraph='').first()
                    sView=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id__isnull=True).first()
                    sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                    sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                subsubsectionSet=models.FormsMapping.objects.values('sub_sub_section__id','sub_sub_section__name','sub_sub_section__code').filter(module_id=module_id,sub_module_id=sub_module_id,section_id=section_id,sub_section__id=subsection['sub_section__id']).distinct('sub_sub_section__id')
                for subsubsection in subsubsectionSet:
                    sub_sub_section_paragraph=''
                    sub_sub_section_view=''
                    if 'project_id' in self.context and self.context['project_id']!='':
                        sPara=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).exclude(paragraph='').first()
                        sView=models.VersionTransaction.objects.values('paragraph','view').filter(version__module_id=module_id,sub_module_id=sub_module_id,project_id=self.context['project_id'],version_id=self.context['version_id'],section_id=section_id,sub_section_id=subsection['sub_section__id'],sub_sub_section_id=subsubsection['sub_sub_section__id']).first()
                        sub_sub_section_paragraph=sPara['paragraph'] if sPara is not None and sPara['paragraph'] is not None else ''
                        sub_sub_section_view=sView['view'] if sView is not None and sView['view'] is not None else True
                    if subsubsection['sub_sub_section__name'] is not None:
                        (subsubsections).append({"id":subsubsection['sub_sub_section__id'],"code":subsubsection['sub_sub_section__code'],"name":subsubsection['sub_sub_section__name'],'sub_module':subModuleDet['id'],'paragraph':sub_sub_section_paragraph,'view':sub_sub_section_view})
                (subsections).append({"id":subsection['sub_section__id'],"code":subsection['sub_section__code'],"name":subsection['sub_section__name'],'paragraph':sub_section_paragraph,'view':sub_section_view,'sub_module':subModuleDet['id'],'subsubsections':subsubsections})
            newReponse['section'].append({"id":section['section__id'],"code":section['section__code'],"name":section['section__name'],'sub_module':subModuleDet['id'],'paragraph':section_paragraph,'view':section_view,'subsections':subsections})

        return newReponse

class GlobalTransactionsSerializer(serializers.ModelSerializer):


    project = projectSerializer(read_only=True)

    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        #print(response,"OOOOOO")
        approved_status = response['approved_status']
        global_transaction=response['id']
        response['global_status'] = masterSerializer.GlobalStatusSerializer(masterModels.GlobalStatus.objects.filter(id = approved_status),many=True).data


        # Form Level #
        form_level_recommender = models.FormLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], status=1, recommender_id=self.context['request'].user.id)

        response['form_level_recommender'] = form_level_recommender

        form_level_approver = models.FormLevelApproverHierarchy.objects.values('form','approver','approver_level','approver_level_status').filter(form_id=response['form'], status=1, approver_id=self.context['request'].user.id)

        response['form_level_approver'] = form_level_approver


        if form_level_recommender:
            if form_level_recommender[0]['recommender_level']>1:
                form_level = form_level_recommender[0]['recommender_level']-1
                pre_form_level_recommender = models.FormLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], status=1, recommender_level=form_level)

                response['pre_form_level_recommender'] = pre_form_level_recommender

            else:
                response['pre_form_level_recommender'] = None

                first_form_level_recommender = models.FormLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], status=1, recommender_level=1)

                response['first_form_level_recommender'] = first_form_level_recommender

        else:

            first_form_level_recommender = models.FormLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], status=1, recommender_level=1)

            response['first_form_level_recommender'] = first_form_level_recommender



        # Project Level #
        project_level_recommender = models.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], project_id=response['project']['id'], status=1, recommender_id=self.context['request'].user.id)

        response['project_level_recommender'] = project_level_recommender

        project_level_approver = models.ProjectLevelApproverHierarchy.objects.values('form','approver','approver_level','approver_level_status').filter(form_id=response['form'], project_id=response['project']['id'], status=1, approver_id=self.context['request'].user.id)

        response['project_level_approver'] = project_level_approver


        if project_level_recommender:
            if project_level_recommender[0]['recommender_level']>1:
                project_level = project_level_recommender[0]['recommender_level']-1
                pre_project_level_recommender = models.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], project_id=response['project']['id'], status=1, recommender_level=project_level)

                response['pre_project_level_recommender'] = pre_project_level_recommender

            else:
                response['pre_project_level_recommender'] = None

                first_project_level_recommender = models.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], project_id=response['project']['id'], status=1, recommender_level=1)

                response['first_project_level_recommender'] = first_project_level_recommender

        else:

            first_project_level_recommender = models.ProjectLevelRecommenderHierarchy.objects.values('form','recommender','recommender_level','recommender_level_status','current_reject').filter(form_id=response['form'], project_id=response['project']['id'], status=1, recommender_level=1)

            response['first_project_level_recommender'] = first_project_level_recommender



        
        type_count = models.ProjectLevelApproverHierarchy.objects.values('approver_id').filter(form_id=response['form'], project_id=response['project']['id']).count()

        if type_count>0:
            response['type_count'] = 'project'
        else:

            type_count = models.FormLevelApproverHierarchy.objects.values('approver_id').filter(form_id=response['form']).count()
            if type_count>0:
                response['type_count'] = 'form'
            else:
                response['type_count'] = None


        gtApprovals = (
                models.GlobalTransactionApproval.objects.values(
                    "status", "approved_on", "comments", "approved_level", "type"
                )
                .filter(transaction_id=response["id"])
                .order_by("id")
        )

        #print(gtApprovals.query,"YYYYYYYYYY")

        gt_initiator = [
                gtApproval
                for gtApproval in gtApprovals
                if gtApproval["approved_level"] == 1 and gtApproval["type"] == 1
            ]
        gt_initiator = (
                gt_initiator[len(gt_initiator) - 1] if gt_initiator else None
            )

        gt_recommendation = [
            gtApproval
            for gtApproval in gtApprovals
            if gtApproval["approved_level"] == 2 and gtApproval["type"] == 1
        ]
        gt_recommendation = (
            gt_recommendation[len(gt_recommendation) - 1]
            if gt_recommendation
            else None
        )

        gt_approver = [
            gtApproval
            for gtApproval in gtApprovals
            if gtApproval["approved_level"] == 3 and gtApproval["type"] == 2
        ]
        gt_approver = (
            gt_approver[len(gt_approver) - 1] if gt_approver else None
        )

        response["gt_initiater"] = gt_initiator
        response["gt_recommendation"] = gt_recommendation
        response["gt_approver"] = gt_approver
        return response


class GlobalTransactionlogSerializer(serializers.ModelSerializer):
    running_id = GlobalTransactionsSerializer(read_only=True)
    class Meta:
        model = models.GlobalTransactionLog
        fields = "__all__" 
class GlobalTransactionDetailsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalTransactionDetailsLog
        fields = "__all__" 
class GlobalTransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalTransactionDetailsLog
        fields = "__all__"
    
### Version ###

class VersionSerializer(serializers.ModelSerializer):
    
    project = projectSerializer(read_only=True)
    class Meta:
        model = models.Version
        fields = "__all__"

class ListVersionSerializer(serializers.ModelSerializer):

    project = projectSerializer(read_only=True)
    module = masterSerializer.ModuleSerializer(read_only = True)
    form = FormsSerializer(read_only = True)

    class Meta:
        model = models.Version
        fields = "__all__" 

    # def to_representation(self, instance):      
    #     response = super().to_representation(instance) 
    #     global_transaction = response['id']
    #     response['details'] = ListGlobalTransactionDetailsSerializer(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction),many=True).data
    #     return response



# class GlobalTransactionResponsibilitySerializer1(serializers.ModelSerializer):

#     directorate = UnitSerializer(read_only=True)
#     project = projectSerializer(read_only=True)
#     section = masterSerializer.GlobalSectionSerializer(read_only = True)

#     class Meta:
#         model = models.GlobalTransactionResponsibility
#         fields = "__all__" 

class GlobalTransactionResponsibilitySerializer(serializers.ModelSerializer):

    directorate = UnitSerializer(read_only=True)
    project = projectSerializer(read_only=True)
    #section = masterSerializer.GlobalSectionSerializer(read_only = True)

    class Meta:
        model = models.GlobalTransactionResponsibility
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        gt_responsibility_master = response['id']
        response['details'] = ListTransactionResponsibilitySerializer(models.GlobalTransactionResponsibilityDetail.objects.filter(gt_responsibility = gt_responsibility_master), many=True).data
        return response


class ListTransactionResponsibilitySerializer(serializers.ModelSerializer):

    # directorate = UnitSerializer(read_only=True)
    # project = projectSerializer(read_only=True)
    section = masterSerializer.GlobalSectionSerializer(read_only = True)
    sub_section = masterSerializer.GlobalSubSectionSerializer(read_only = True)
    sub_sub_section = masterSerializer.GlobalSubSubSectionSerializer(read_only = True)
    # module = masterSerializer.ModuleSerializer(read_only = True)
    sub_module = masterSerializer.SubModuleSerializer(read_only = True)
    
    
    class Meta:
        model = models.GlobalTransactionResponsibilityDetail
        fields = "__all__" 



class ListTransactionResponsibilitySerializerDummy(serializers.ModelSerializer):
    
    
    class Meta:
        model = models.GlobalTransactionResponsibilityDetail
        fields = "__all__" 


    def to_representation(self, instance):        
        response = super().to_representation(instance)
        #print(response,"GGGGGGGRRRRR")


        sectionSet = models.GlobalTransactionResponsibilityDetail.objects.values('module_id','section__id','section__name','section__code').filter(project_id='123').distinct('directorate_id')

        for section in sectionSet:
            sPara=models.GlobalSection.objects.values('name').filter(module_id=section['module_id'])

        print(sPara)


class GlobalTransactionCommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalTransactionComments
        fields = "__all__"

class ListGlobalTransactionCommentsSerializer(serializers.ModelSerializer):

    module = masterSerializer.ModuleSerializer(read_only = True)
    class Meta:
        model = models.GlobalTransactionComments
        fields = "__all__" 

    # def to_representation(self, instance):        
    #     response = super().to_representation(instance) 
    #     global_transaction = response['id']
    #     response['details'] = ListGlobalTransactionDetailsSerializer(models.GlobalTransactionDetails.objects.filter(global_transaction_id = global_transaction),many=True).data
    #     return response
class DashboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalTransaction
        fields = "__all__" 

    def to_representation(self, instance):        
        response = super().to_representation(instance)
        response['project'] = ListProjectSerializer(masterModels.Project.objects.filter(id=response['project']),many=True).data        
        return response

class ProjectLogSerializer(serializers.ModelSerializer):
    project = projectSerializer(read_only=True)
    class Meta:
        model = models.ProjectLog
        fields = "__all__"


## Forms ##
class AllFormsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Forms
        #fields = "__all__"
        fields = ['id','name','status']

class AllFormsMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormsMapping
        #fields = ['id', 'form_id','Class_id','module_id','sub_module_id','section_id','sub_section_id','sub_sub_section_id','order']
        fields = "__all__"


# Ship #
class ShipDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.GlobalTransactionShipDetail
        fields = "__all__"        


################### Dock Yard ###################

class DartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dart
        fields = "__all__"

class ListDartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dart
        fields = "__all__" 

class RASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RA
        fields = "__all__"

class ListRASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RA
        fields = "__all__" 

class OPDEFSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OPDEF
        fields = "__all__"

class ListOPDEFSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OPDEF
        fields = "__all__" 

class WorkInstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkInstruction
        fields = "__all__"

class ListWorkInstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkInstruction
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        dart_id = response['dart']
        refit_type_id = response['refit_type']
        response['dart_det'] = models.Dart.objects.values('id','SrNo').filter(id=dart_id).first()
        response['refit_type_det'] = masterModels.RefitType.objects.values('id','name').filter(id=refit_type_id).first()
        return response

class WorkInstructionQCCheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkInstructionQCCheck
        fields = "__all__"

class JobCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobCard
        fields = "__all__"

class ListJobCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobCard
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        work_instruction_id = response['work_instruction']
        response['work_instruction_id_det'] = models.WorkInstruction.objects.values('id','name').filter(id=work_instruction_id).first()
        return response

class JobCardQCCheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobCardQCCheck
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attendance
        fields = "__all__"

class ListAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attendance
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance) 
        user_id = response['user']
        center_id = response['center']
        response['user_det'] = masterAccounts.User.objects.values('id','loginname').filter(id=user_id).first()
        response['center_det'] = models.Center.objects.values('id','name').filter(id=center_id).first()
        return response


class MonthlyCreditsDebitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyCreditsDebits
        fields = "__all__"


class ListMonthlyCreditsDebitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonthlyCreditsDebits
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user_id = response['user']
        allowance_id = response['allowance']
        deduction_id = response['deduction']
        response['user_det'] = masterAccounts.User.objects.values('id','loginname').filter(id=user_id).first()
        response['allowance_det'] = models.AllowancesMaster.objects.values('id','name').filter(id=allowance_id).first()
        response['deduction_det'] = models.DeductionsMaster.objects.values('id','name').filter(id=deduction_id).first()
        return response