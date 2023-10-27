from gettext import Catalog
from importlib.resources import Package
from inspect import Signature
from itertools import product
from operator import mod
from pyexpat import model
from tabnanny import verbose
# from xml.dom.minidom import DocumentType
from django.db import models
from django.db.models.deletion import CASCADE
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User
#from master.models import Project
from master.models import Project, Section, Unit, Compartment, System, Equipment, Module, SubModule, GlobalSection, GlobalSubSection, GlobalSubSubSection, Class, Command, Department, RefitType, Center, AllowancesMaster, DeductionsMaster, OverTime, Shopfloor, StatusMaster
from access.models import AccessUserRoles,ProcessFlow


class SSS(models.Model):
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
        db_table = 'master.sss'
        verbose_name = 'sss'
        verbose_name_plural = 'sss'

class PSRSection(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=255,null=True)
    sequence = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')),default=1)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.psr_section'
        verbose_name = 'psr_section'
        verbose_name_plural = 'psr_section'

class PSRSectionUnit(models.Model):
    section = models.ForeignKey(PSRSection, on_delete= models.CASCADE,null=True)
    unit = models.ForeignKey(Unit, on_delete= models.CASCADE,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'master.psr_section_unit'
        verbose_name = 'psr_section_unit'
        verbose_name_plural = 'psr_section_unit'

class PSRSubSection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=15)
    section = models.ForeignKey(PSRSection, on_delete= models.CASCADE,null=True)
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
        db_table = 'master.psr_sub_section'
        verbose_name = 'psr_sub_section'
        verbose_name_plural = 'psr_sub_section'


class PSRUnitCompartments(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    section_unit = models.ForeignKey(PSRSectionUnit, on_delete=models.CASCADE,null=True)
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mapping.psr_unit_compartment'
        verbose_name = 'psr_unit_compartment'
        verbose_name_plural = 'psr_unit_compartment'

class PSRUnitEquipments(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    section_unit = models.ForeignKey(PSRSectionUnit, on_delete=models.CASCADE,null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mapping.psr_unit_equipments'
        verbose_name = 'psr_unit_equipments'
        verbose_name_plural = 'psr_unit_equipments'


class PSRUnitSystems(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    section_unit = models.ForeignKey(PSRSectionUnit, on_delete=models.CASCADE,null=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mapping.psr_unit_systems'
        verbose_name = 'psr_unit_systems'
        verbose_name_plural = 'psr_unit_systems'

class PrimaryRoles(models.Model):
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
        db_table = 'master.psr_primary_roles'
        verbose_name = 'psr_primary_roles'
        verbose_name_plural = 'psr_primary_roles'


class SecondaryRoles(models.Model):
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
        db_table = 'master.psr_secondary_roles'
        verbose_name = 'psr_secondary_roles'
        verbose_name_plural = 'psr_secondary_roles'

class Standard(models.Model):
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
        db_table = 'master.psr_standard'
        verbose_name = 'psr_standard'
        verbose_name_plural = 'psr_standard'

class PlanForManpowerInduction(models.Model):
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
        db_table = 'master.psr_plan_for_manpower_induction'
        verbose_name = 'psr_plan_for_manpower_induction'
        verbose_name_plural = 'psr_plan_for_manpower_induction'

class AcquisitionMethod(models.Model):
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
        db_table = 'master.psr_acquisition_method'
        verbose_name = 'psr_acquisition_method'
        verbose_name_plural = 'psr_acquisition_method'

# Initiation Notes
class InitiationNotes(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    primary_role = models.TextField(blank=True, null=True)
    secondary_role = models.TextField(blank=True, null=True)
    budgeted_cost_per_platform = models.DecimalField(max_digits = 6, decimal_places = 2,null=True,blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, null=True)
    plan_for_manpower_induction = models.ForeignKey(PlanForManpowerInduction, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    acquisition_method = models.ForeignKey(AcquisitionMethod, on_delete=models.CASCADE, null=True)
    remarks = models.TextField(null=True, blank=True)

    accord_of_aon = models.DateField(null=True, blank=True)
    conclusion_of_contract = models.DateField(null=True, blank=True)
    induction = models.DateField(null=True, blank=True)
    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)


    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.remarks

    class Meta:
        db_table = 'psr.initiation_notes'
        verbose_name = 'InitiationNotes'
        verbose_name_plural = 'InitiationNotes'

# Initiation Notes Upload Document
class InitiationNotesDocument(models.Model):

    initiation_notes = models.ForeignKey(InitiationNotes, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='initiation_notes_document/', null=True, blank=True)

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
        db_table = 'psr.initiation_notes_document'
        verbose_name = 'InitiationNotesDocument'
        verbose_name_plural = 'InitiationNotesDocument'

# Initiation Notes Send Mail
class InitiationNotesSendMail(models.Model):

    initiation_notes = models.ForeignKey(InitiationNotes, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='initiation_notes_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.initiation_notes_send_email'
        verbose_name = 'InitiationNotesSendEmail'
        verbose_name_plural = 'InitiationNotesSendEmail'

# PSR Formulation Of Approach Paper
class FormulationOfApproachPaper(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    remarks = models.TextField(null=True, blank=True)
    intoduction = models.TextField(null=True, blank=True)
    critical_design_driver = models.TextField(null=True, blank=True)
    weapons_and_sensors = models.TextField(null=True, blank=True)
    composite_communication_capability = models.TextField(null=True, blank=True)
    flag_platform = models.TextField(null=True, blank=True)
    speed_and_endurance = models.TextField(null=True, blank=True)
    operations_cycle = models.TextField(null=True, blank=True)
    stealth = models.TextField(null=True, blank=True)
    redundancy = models.TextField(null=True, blank=True)
    aviation = models.TextField(null=True, blank=True)
    autonomous_systems = models.TextField(null=True, blank=True)
    unrep = models.TextField(null=True, blank=True)
    survivability = models.TextField(null=True, blank=True)
    medical_and_hadr_facilities = models.TextField(null=True, blank=True)
    boats_and_landing_craft = models.TextField(null=True, blank=True)
    upper_deck_equipment = models.TextField(null=True, blank=True)
    habitability = models.TextField(null=True, blank=True)
    nbcd_compliance = models.TextField(null=True, blank=True)
    special_capabilities = models.TextField(null=True, blank=True)
    manpower = models.TextField(null=True, blank=True)
    project_activity_description = models.TextField(null=True, blank=True)

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)


    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.formulation_of_approach_paper'
        verbose_name = 'FormulationOfApproachPaper'
        verbose_name_plural = 'FormulationOfApproachPaper'

# PSR Formulation Of Approach Paper Upload Document
class FormulationOfApproachPaperDocument(models.Model):

    formulation_of_approach_paper = models.ForeignKey(FormulationOfApproachPaper, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='formulation_of_approach_paper_document/', null=True, blank=True)

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
        db_table = 'psr.formulation_of_approach_paper_document'
        verbose_name = 'FormulationOfApproachPaperDocument'
        verbose_name_plural = 'FormulationOfApproachPaperDocument'

# PSR Formulation Of Approach Paper Send Mail
class FormulationOfApproachPaperSendMail(models.Model):

    formulation_of_approach_paper = models.ForeignKey(FormulationOfApproachPaper, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='formulation_of_approach_paper_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.formulation_of_approach_paper_send_email'
        verbose_name = 'FormulationOfApproachPaperSendMail'
        verbose_name_plural = 'FormulationOfApproachPaperSendMail'

class FormulationOfApproachPaperResponsibility(models.Model):

    
    formulation_of_approach_paper = models.ForeignKey(FormulationOfApproachPaper, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    #section = models.ForeignKey(Section, on_delete=models.CASCADE,null=True)
    #unit = models.ForeignKey(Unit, on_delete=models.CASCADE,null=True)
    section = models.TextField(blank=True, null=True)
    unit = models.TextField( blank=True, null=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.formulation_of_approach_paper_responsibility'
        verbose_name = 'FormulationOfApproachPaperResponsibility'
        verbose_name_plural = 'FormulationOfApproachPaperResponsibility'

class FormulationOfApproachPaperResponsibilityCompartment(models.Model):

    formulation_of_approach_paper_responsibility = models.ForeignKey(FormulationOfApproachPaperResponsibility, on_delete=models.CASCADE,null=True)
    #compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE,null=True)
    compartment = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.compartment

    class Meta:
        db_table = 'psr.formulation_of_approach_paper_responsibility_compartment'
        verbose_name = 'FormulationOfApproachPaperResponsibilityCompartment'
        verbose_name_plural = 'FormulationOfApproachPaperResponsibilityCompartment'

class FormulationOfApproachPaperResponsibilitySystem(models.Model):

    formulation_of_approach_paper_responsibility = models.ForeignKey(FormulationOfApproachPaperResponsibility, on_delete=models.CASCADE,null=True)
    #system = models.ForeignKey(System, on_delete=models.CASCADE,null=True)
    system = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.system

    class Meta:
        db_table = 'psr.formulation_of_approach_paper_responsibility_system'
        verbose_name = 'FormulationOfApproachPaperResponsibilitySystem'
        verbose_name_plural = 'FormulationOfApproachPaperResponsibilitySystem'

class FormulationOfApproachPaperResponsibilityEquipment(models.Model):

    formulation_of_approach_paper_responsibility = models.ForeignKey(FormulationOfApproachPaperResponsibility, on_delete=models.CASCADE,null=True)
    #equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True)
    equipment = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.equipment

    class Meta:
        db_table = 'psr.formulation_of_approach_paper_responsibility_equipment'
        verbose_name = 'FormulationOfApproachPaperResponsibilityEquipment'
        verbose_name_plural = 'FormulationOfApproachPaperResponsibilityEquipment'


# PSR Presentation Of Approach Paper
class PresentationOfApproachPaper(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    file_name = models.FileField(upload_to='presentation_of_approach_paper/', null=True, blank=True)

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.presentation_of_approach_paper'
        verbose_name = 'PresentationOfApproachPaper'
        verbose_name_plural = 'PresentationOfApproachPaper'

# PSR Presentation Of Approach Paper Upload Document
class PresentationOfApproachPaperDocument(models.Model):

    presentation_of_approach_paper = models.ForeignKey(PresentationOfApproachPaper, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='presentation_of_approach_paper_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'psr.presentation_of_approach_paper_document'
        verbose_name = 'PresentationOfApproachPaperDocument'
        verbose_name_plural = 'PresentationOfApproachPaperDocument'

# PSR Presentation Of Approach Paper Send Mail
class PresentationOfApproachPaperSendMail(models.Model):

    presentation_of_approach_paper = models.ForeignKey(PresentationOfApproachPaper, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='presentation_of_approach_paper_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.presentation_of_approach_paper_send_email'
        verbose_name = 'PresentationOfApproachPaperSendMail'
        verbose_name_plural = 'PresentationOfApproachPaperSendMail'


# PSR Inputs for Staff Requirement
class InputsForStaffRequirement(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.inputs_for_staff_requirements'
        verbose_name = 'InputsForStaffRequirements'
        verbose_name_plural = 'InputsForStaffRequirements'


# PSR Inputs for Staff Requirement Upload Document
class InputsForStaffRequirementDocument(models.Model):

    inputs_for_staff_requirement = models.ForeignKey(InputsForStaffRequirement, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='inputs_for_staff_requirement/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'psr.inputs_for_staff_requirement_document'
        verbose_name = 'InputsforStaffRequirementDocument'
        verbose_name_plural = 'InputsforStaffRequirementDocument'

# PSR Inputs for Staff Requirement Send Mail
class InputsForStaffRequirementSendMail(models.Model):

    inputs_for_staff_requirement = models.ForeignKey(InputsForStaffRequirement, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='inputs_for_staff_requirement/', null=True, blank=True)
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
        db_table = 'psr.inputs_for_staff_requirement_send_email'
        verbose_name = 'InputsforStaffRequirementSendMail'
        verbose_name_plural = 'InputsforStaffRequirementSendMail'

class PSRDataFlow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True) 
    psr_section = models.ForeignKey(PSRSection, on_delete=models.CASCADE,null=True) 
    standards = models.TextField(null=True, blank=True)
    whole_ship_features = models.TextField(null=True, blank=True)
    man_power = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.data_flow'
        verbose_name = 'data_flow'
        verbose_name_plural = 'data_flow'

class PSRDataFlowCompartment(models.Model):
    data_flow = models.ForeignKey(PSRDataFlow, on_delete=models.CASCADE,null=True)
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE,null=True)
    ser =models.TextField(null=True, blank=True)
    name =models.TextField(null=True, blank=True)
    numbers =models.TextField(null=True, blank=True)
    location =models.TextField(null=True, blank=True)
    equipment =models.TextField(null=True, blank=True)
    features =models.TextField(null=True, blank=True)
    layout =models.TextField(null=True, blank=True)
    special_requirements =models.TextField(null=True, blank=True)
    standards =models.TextField(null=True, blank=True)
    recommendations =models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.data_flow_compartment'
        verbose_name = 'data_flow_compartment'
        verbose_name_plural = 'data_flow_compartment'

class PSRDataFlowEquipments(models.Model):
    data_flow = models.ForeignKey(PSRDataFlow, on_delete=models.CASCADE,null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True)
    ser =models.TextField(null=True, blank=True)
    name =models.TextField(null=True, blank=True)
    numbers =models.TextField(null=True, blank=True)
    capabilities =models.TextField(null=True, blank=True)
    weight =models.TextField(null=True, blank=True)
    location =models.TextField(null=True, blank=True)
    interface =models.TextField(null=True, blank=True)
    procurement =models.TextField(null=True, blank=True)
    vendor =models.TextField(null=True, blank=True)
    cost =models.TextField(null=True, blank=True)
    standards =models.TextField(null=True, blank=True)
    sustence =models.TextField(null=True, blank=True)
    recommendations =models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.data_flow_equipments'
        verbose_name = 'data_flow_equipments'
        verbose_name_plural = 'data_flow_equipments'

class PSRDataFlowsystems(models.Model):
    data_flow = models.ForeignKey(PSRDataFlow, on_delete=models.CASCADE,null=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE,null=True)
    ser =models.TextField(null=True, blank=True)
    name =models.TextField(null=True, blank=True)
    numbers =models.TextField(null=True, blank=True)
    capabilities =models.TextField(null=True, blank=True)
    weight =models.TextField(null=True, blank=True)
    location =models.TextField(null=True, blank=True)
    interface =models.TextField(null=True, blank=True)
    procurement =models.TextField(null=True, blank=True)
    vendor =models.TextField(null=True, blank=True)
    cost =models.TextField(null=True, blank=True)
    standards =models.TextField(null=True, blank=True)
    sustence =models.TextField(null=True, blank=True)
    recommendations =models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.data_flow_systems'
        verbose_name = 'data_flow_systems'
        verbose_name_plural = 'data_flow_systems'

# PSR Inputs for Staff Requirement
class InputsSRSSR(models.Model):

    sr_id = models.ForeignKey(InputsForStaffRequirement, on_delete=models.CASCADE,null=True)
    sss = models.ForeignKey(SSS, on_delete=models.CASCADE,null=True)
    specification = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.inputs_sr_ssr'
        verbose_name = 'inputs_sr_ssr'
        verbose_name_plural = 'inputs_sr_ssr'

class InputsForStaffRequirementCompartment(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    ser = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    numbers = models.TextField(null=True, blank=True)
    weight_volume_and_power_consumption = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    equipment = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)

    layout = models.TextField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)
    standards = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.inputs_for_staff_requirements_compartment'
        verbose_name = 'InputsForStaffRequirementCompartment'
        verbose_name_plural = 'InputsForStaffRequirementCompartment'


class InputsForStaffRequirementEquipment(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    ser = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    numbers = models.TextField(null=True, blank=True)
    weight_volume_and_power_consumption = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    equipment = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)

    layout = models.TextField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)
    standards = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.inputs_for_staff_requirements_equipment'
        verbose_name = 'InputsForStaffRequirementEquipment'
        verbose_name_plural = 'InputsForStaffRequirementEquipment'


class InputsForStaffRequirementSystem(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    ser = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    numbers = models.TextField(null=True, blank=True)
    weight_volume_and_power_consumption = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    equipment = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)

    layout = models.TextField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)
    standards = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.inputs_for_staff_requirements_system'
        verbose_name = 'InputsForStaffRequirementSystem'
        verbose_name_plural = 'InputsForStaffRequirementSystem'



# PSR Concept Design
class ConceptDesign(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    refinement_of_values = models.TextField(null=True, blank=True)
    powering_requirements = models.TextField(null=True, blank=True)
    total_heat_load_calculation = models.TextField(null=True, blank=True)

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.concept_design'
        verbose_name = 'ConceptDesign'
        verbose_name_plural = 'ConceptDesign'

# PSR Concept Design Upload Document
class ConceptDesignDocument(models.Model):

    concept_design = models.ForeignKey(ConceptDesign, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='concept_design_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'psr.concept_design_document'
        verbose_name = 'ConceptDesignDocument'
        verbose_name_plural = 'ConceptDesignDocument'



# PSR Concept Design Send Mail
class ConceptDesignSendMail(models.Model):

    concept_design = models.ForeignKey(ConceptDesign, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='concept_design_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.concept_design_send_email'
        verbose_name = 'ConceptDesignSendMail'
        verbose_name_plural = 'ConceptDesignSendMail'



# PSR Incorporation of Design Inputs
class IncorporationOfDesignInputs(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    cost_estimation = models.TextField(null=True, blank=True)

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.incorporation_of_design_inputs'
        verbose_name = 'IncorporationOfDesignInputs'
        verbose_name_plural = 'IncorporationOfDesignInputs'

# PSR Incorporation Of Design Inputs Document
class IncorporationOfDesignInputsDocument(models.Model):

    incorporation_of_design_inputs = models.ForeignKey(IncorporationOfDesignInputs, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='incorporation_of_design_inputs_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'psr.incorporation_of_design_inputs_document'
        verbose_name = 'IncorporationOfDesignInputsDocument'
        verbose_name_plural = 'IncorporationOfDesignInputsDocument'



# PSR Incorporation Of Design Inputs Send Mail
class IncorporationOfDesignInputsSendMail(models.Model):

    incorporation_of_design_inputs = models.ForeignKey(IncorporationOfDesignInputs, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='incorporation_of_design_inputs_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.incorporation_of_design_inputs_send_email'
        verbose_name = 'IncorporationOfDesignInputsSendMail'
        verbose_name_plural = 'IncorporationOfDesignInputsSendMail'




# PSR Receipt Of RFI Responses
class ReceiptOfRFIResponses(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    file_name = models.FileField(upload_to='receipt_of_rfi_responses/', null=True, blank=True)

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.receipt_of_rfi_responses'
        verbose_name = 'ReceiptOfRFIResponses'
        verbose_name_plural = 'ReceiptOfRFIResponses'

# PSR Receipt Of RFI Responses Upload Document
class ReceiptOfRFIResponsesDocument(models.Model):

    receipt_of_rfi_responses = models.ForeignKey(ReceiptOfRFIResponses, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='receipt_of_rfi_responses_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'psr.receipt_of_rfi_responses_document'
        verbose_name = 'ReceiptOfRFIResponsesDocument'
        verbose_name_plural = 'ReceiptOfRFIResponsesDocument'



# PSR Receipt Of RFI Responses Send Mail
class ReceiptOfRFIResponsesSendMail(models.Model):

    receipt_of_rfi_responses = models.ForeignKey(ReceiptOfRFIResponses, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='receipt_of_rfi_responses_email_attachment/', null=True, blank=True)
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
        db_table = 'psr.receipt_of_rfi_responses_send_email'
        verbose_name = 'ReceiptOfRFIResponsesSendMail'
        verbose_name_plural = 'ReceiptOfRFIResponsesSendMail'

class DocumentSections(models.Model):
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
        db_table = 'master.gls_document_sections'
        verbose_name = 'gls_document_sections'
        verbose_name_plural = 'gls_document_sections'

class DocumentSubSections(models.Model):
    document_sections = models.ForeignKey(DocumentSections, on_delete=models.CASCADE,null=True)
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
        db_table = 'master.gls_document_sub_sections'
        verbose_name = 'gls_document_sub_sections'
        verbose_name_plural = 'gls_document_sub_sections'

class DocumentSubSections2(models.Model):
    document_sections = models.ForeignKey(DocumentSections, on_delete=models.CASCADE,null=True)
    document_sub_sections = models.ForeignKey(DocumentSubSections, on_delete=models.CASCADE,null=True)
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
        db_table = 'master.gls_document_sub_sections2'
        verbose_name = 'gls_document_sub_sections2'
        verbose_name_plural = 'gls_document_sub_sections2'

class Annexures(models.Model):
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
        db_table = 'master.gls_annexures'
        verbose_name = 'gls_annexures'
        verbose_name_plural = 'gls_annexures'

# GLS -- Initiation Notes
class InitiationNotesGLSMaster(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    type_name = models.SmallIntegerField(choices=((1,'Section'),(2,'Annexure')))

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

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
        db_table = 'gls.initiation_notes_master'
        verbose_name = 'GLS Initiation Notes Master'
        verbose_name_plural = 'GLS Initiation Notes Master'

class InitiationNotesGLS(models.Model):

    initiation_notes_gls_master = models.ForeignKey(InitiationNotesGLSMaster, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    type_name = models.SmallIntegerField(choices=((1,'Section'),(2,'Annexure')))

    document_sections = models.ForeignKey(DocumentSections, on_delete=models.CASCADE,null=True)
    document_sub_sections = models.ForeignKey(DocumentSubSections, on_delete=models.CASCADE,null=True)
    document_sub_sections2 = models.ForeignKey(DocumentSubSections2, on_delete=models.CASCADE,null=True)
    annexures = models.ForeignKey(Annexures, on_delete=models.CASCADE,null=True)
    paragraph_title = models.CharField(max_length=255, blank=True, null=True)
    paragraph = models.TextField(null=True, blank=True)
    primary = models.IntegerField(null=True)
    secondary1 = models.IntegerField(null=True)
    secondary2 = models.IntegerField(null=True)
    secondary3 = models.IntegerField(null=True)


    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    start_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.paragraph_title

    class Meta:
        db_table = 'gls.initiation_notes'
        verbose_name = 'GLS Initiation Notes'
        verbose_name_plural = 'GLS Initiation Notes'

# GLS Initiation Notes Upload Document
class GLSInitiationNotesDocument(models.Model):

    initiation_notes_gls_master = models.ForeignKey(InitiationNotesGLSMaster, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='gls_initiation_notes_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gls.gls_initiation_notes_document'
        verbose_name = 'GLSInitiationNotesDocument'
        verbose_name_plural = 'GLSInitiationNotesDocument'



# GLS Initiation Notes Send Mail
class GLSInitiationNotesSendMail(models.Model):

    initiation_notes_gls_master = models.ForeignKey(InitiationNotesGLSMaster, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='gls_initiation_notes_email_attachment/', null=True, blank=True)
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
        db_table = 'gls.gls_initiation_notes_send_email'
        verbose_name = 'GLSInitiationNotesSendMail'
        verbose_name_plural = 'GLSInitiationNotesSendMail'


# BLS -- Initiation Notes
class InitiationNotesBLSMaster(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    type_name = models.SmallIntegerField(choices=((1,'Section'),(2,'Annexure')))

    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)
    
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
        db_table = 'bls.initiation_notes_master'
        verbose_name = 'BLS Initiation Notes Master'
        verbose_name_plural = 'BLS Initiation Notes Master'

class InitiationNotesBLS(models.Model):

    initiation_notes_bls_master = models.ForeignKey(InitiationNotesBLSMaster, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    type_name = models.SmallIntegerField(choices=((1,'Section'),(2,'Annexure')))

    document_sections = models.ForeignKey(DocumentSections, on_delete=models.CASCADE,null=True)
    document_sub_sections = models.ForeignKey(DocumentSubSections, on_delete=models.CASCADE,null=True)
    document_sub_sections2 = models.ForeignKey(DocumentSubSections2, on_delete=models.CASCADE,null=True)
    annexures = models.ForeignKey(Annexures, on_delete=models.CASCADE,null=True)
    paragraph_title = models.CharField(max_length=255, blank=True, null=True)
    paragraph = models.TextField(null=True, blank=True)
    primary = models.IntegerField(null=True)
    secondary1 = models.IntegerField(null=True)
    secondary2 = models.IntegerField(null=True)
    secondary3 = models.IntegerField(null=True)


    # Approval
    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    start_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.paragraph_title

    class Meta:
        db_table = 'bls.initiation_notes'
        verbose_name = 'BLS Initiation Notes'
        verbose_name_plural = 'BLS Initiation Notes'


class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/GLS/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)
    

    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'gls.excel_file_upload'
        verbose_name = 'GLS Excel File Upload'
        verbose_name_plural = 'GLS Excel File Upload'

# BLS Initiation Notes Upload Document
class BLSInitiationNotesDocument(models.Model):

    initiation_notes_bls_master = models.ForeignKey(InitiationNotesBLSMaster, on_delete=models.CASCADE,null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_remark = models.CharField(max_length=255, blank=True, null=True)

    file_name = models.FileField(upload_to='bls_initiation_notes_document/', null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #created_ip = models.GenericIPAddressField()
    created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bls.bls_initiation_notes_document'
        verbose_name = 'BLSInitiationNotesDocument'
        verbose_name_plural = 'BLSInitiationNotesDocument'



# BLS Initiation Notes Send Mail
class BLSInitiationNotesSendMail(models.Model):

    initiation_notes_bls_master = models.ForeignKey(InitiationNotesBLSMaster, on_delete=models.CASCADE,null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(null=True,blank=True)
    file_name = models.FileField(upload_to='bls_initiation_notes_email_attachment/', null=True, blank=True)
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
        db_table = 'bls.bls_initiation_notes_send_email'
        verbose_name = 'BLSInitiationNotesSendMail'
        verbose_name_plural = 'BLSInitiationNotesSendMail'


# General Section


class PSRDataFlowGeneralSection(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True) 
    #psr_section = models.ForeignKey(PSRSection, on_delete=models.CASCADE,null=True) 
    roles = models.TextField(null=True, blank=True)
    critical_design_drivers = models.TextField(null=True, blank=True)
    operating_philosophy = models.TextField(null=True, blank=True)
    area_of_operations = models.TextField(null=True, blank=True)
    rules_and_regulations = models.TextField(null=True, blank=True)
    general_remarks = models.TextField(null=True, blank=True)
    displacement = models.TextField(null=True, blank=True)
    dimensions = models.TextField(null=True, blank=True)
    speed = models.TextField(null=True, blank=True)
    endurance_and_range = models.TextField(null=True, blank=True)
    sea_worthiness = models.TextField(null=True, blank=True)
    propulsion = models.TextField(null=True, blank=True)
    operating_conditions = models.TextField(null=True, blank=True)
    design_and_construction_standards = models.TextField(null=True, blank=True)
    stealth = models.TextField(null=True, blank=True)
    ergonomics = models.TextField(null=True, blank=True)
    complement = models.TextField(null=True, blank=True)
    cots_technology = models.TextField(null=True, blank=True)
    protection = models.TextField(null=True, blank=True)
    unrep = models.TextField(null=True, blank=True)
    boats_and_usvs = models.TextField(null=True, blank=True)
    noise_reduction = models.TextField(null=True, blank=True)
    op_logistic_management_information_system = models.TextField(null=True, blank=True)
    ipms = models.TextField(null=True, blank=True)
    surveillance_and_security_arrangement = models.TextField(null=True, blank=True)
    cim = models.TextField(null=True, blank=True)
    green_warship = models.TextField(null=True, blank=True)
    construction = models.TextField(null=True, blank=True)
    automation_and_redundancy = models.TextField(null=True, blank=True)
    workshops = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.data_flow_general_section'
        verbose_name = 'data_flow_general_section'
        verbose_name_plural = 'data_flow_general_section'



class ProjectModuleMaster(models.Model):

    name = models.CharField(max_length=250)
    display_name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dashboard.project_module_master'
        verbose_name = 'project_module_master'
        verbose_name_plural = 'project_module_master'

class ProjectModuleStatus(models.Model):

    project_module_master = models.ForeignKey(ProjectModuleMaster, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    status = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dashboard.project_module_status'
        verbose_name = 'project_module_status'
        verbose_name_plural = 'project_module_status'

######## Forms Mapping ##############

class Forms(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
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
        db_table = 'psr.forms'
        verbose_name = 'psr_forms'
        verbose_name_plural = 'psr_forms'


class DataAccessForms(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "access.data_access_forms"
        verbose_name = "Data Access Form"
        verbose_name_plural = "Data Access Forms"
        #unique_together = ("user", "module", "sub_module")
        unique_together = ("user", "form")

class FormsMapping(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class,on_delete=models.CASCADE,default=13)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    #code = models.CharField(max_length=15)
    order = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    #created_ip = models.GenericIPAddressField(default='192.168.0.1')
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'psr.forms_mapping'
        verbose_name = 'forms_mapping'
        verbose_name_plural = 'forms_mapping'

class GlobalTransaction(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    form =  models.ForeignKey(Forms, on_delete = models.CASCADE,null=True)

    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)
    initiater = models.SmallIntegerField(null=True, blank=True)
    recommender = models.SmallIntegerField(null=True, blank=True)
    approver = models.SmallIntegerField(null=True, blank=True)
    approved_level = models.SmallIntegerField(default=1)

    recommender_level = models.SmallIntegerField(null=True, blank=True)
    approver_level = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'psr.global_transaction'
        verbose_name = 'global_transaction'
        verbose_name_plural = 'global_transaction'

class GlobalTransactionApproval(models.Model):
    transaction = models.ForeignKey(GlobalTransaction, on_delete=models.CASCADE, null=True)
    comments = models.TextField(null=True, blank=True)
    type = models.SmallIntegerField(
        choices=((1,'initiator'), (2, "Recommendation"), (3, "Approval")), null=True, blank=True
    )
    status = models.SmallIntegerField(choices=((1, "Approved"), (2, "Rejected")), null=True, blank=True)
    approved_role = models.ForeignKey(AccessUserRoles, on_delete=models.CASCADE, null=True)
    approved_level = models.SmallIntegerField(null=True)
    approved_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    approved_ip = models.GenericIPAddressField(null=True)

    def __int__(self):
        return self.transaction

    class Meta:
        db_table = 'transaction.global_transaction_approval'
        verbose_name = 'global_transaction_approval'
        verbose_name_plural = 'global_transaction_approvals'

class GlobalTransactionLog(models.Model):

    
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    form =  models.ForeignKey(Forms, on_delete = models.CASCADE,null=True)

    approved_status = models.IntegerField(null=True, blank=True)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateField(null=True, blank=True)
    approved_remark = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'log.global_transaction'
        verbose_name = 'global_transactionlog'
        verbose_name_plural = 'global_transactionlog'

class GlobalTransactionDetails(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    global_transaction =  models.ForeignKey(GlobalTransaction, on_delete = models.CASCADE)
    sub_module =  models.ForeignKey(SubModule, on_delete = models.CASCADE)

    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    paragraph = models.TextField(null=True,blank=True)
    para_no = models.CharField(max_length=100, blank=True, null=True)
    view = models.BooleanField(default=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return (self.global_transaction) or ''

    class Meta:
        db_table = 'psr.global_transaction_details'
        verbose_name = 'global_transaction_details'
        verbose_name_plural = 'global_transaction_details'

class GlobalTransactionDetailsLog(models.Model):

    
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    global_transaction =  models.ForeignKey(GlobalTransaction, on_delete = models.CASCADE)
    sub_module =  models.ForeignKey(SubModule, on_delete = models.CASCADE)

    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    paragraph = models.TextField(null=True,blank=True)
    para_no = models.CharField(max_length=100, blank=True, null=True)
    view = models.BooleanField(default=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)  

    def __str__(self):
        return self.global_transaction

    class Meta:
        db_table = 'log.global_transaction_details'
        verbose_name = 'global_transaction_detailslog'
        verbose_name_plural = 'global_transaction_detailslog'
class SSSMapping(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'psr.sss_mapping'
        verbose_name = 'sss_mapping'
        verbose_name_plural = 'sss_mapping'


#### Version ####
class Version(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    form =  models.ForeignKey(Forms, on_delete = models.CASCADE,null=True)
    version = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.version'
        verbose_name = 'version'
        verbose_name_plural = 'version'


class VersionTransaction(models.Model):

    version = models.ForeignKey(Version, on_delete=models.CASCADE,null=True) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    global_transaction =  models.ForeignKey(GlobalTransaction, on_delete = models.CASCADE)
    sub_module =  models.ForeignKey(SubModule, on_delete = models.CASCADE)

    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    paragraph = models.TextField(null=True,blank=True)
    view = models.BooleanField(default=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.version

    class Meta:
        db_table = 'psr.version_details'
        verbose_name = 'version_details'
        verbose_name_plural = 'version_details'



class GlobalTransactionResponsibility(models.Model):

    directorate = models.ForeignKey(Unit, on_delete= models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    #section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.directorate

    class Meta:
        db_table = 'psr.global_transaction_responsibility'
        verbose_name = 'global_transaction_responsibility'
        verbose_name_plural = 'global_transaction_responsibility'

class GlobalTransactionResponsibilityDetail(models.Model):

    gt_responsibility = models.ForeignKey(GlobalTransactionResponsibility, on_delete=models.CASCADE,null=True) 
    directorate = models.ForeignKey(Unit, on_delete= models.CASCADE,null=True)
    module =  models.ForeignKey(Module, on_delete = models.CASCADE)
    sub_module =  models.ForeignKey(SubModule, on_delete = models.CASCADE)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True) 

    def __str__(self):
        return self.directorate

    class Meta:
        db_table = 'psr.global_transaction_responsibility_detail'
        verbose_name = 'global_transaction_responsibility_detail'
        verbose_name_plural = 'global_transaction_responsibility_detail'



class GlobalTransactionComments(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    #global_transaction =  models.ForeignKey(GlobalTransaction, on_delete = models.CASCADE)
    #global_transaction_detail_id = models.IntegerField(null=True)
    comments = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.module

    class Meta:
        db_table = 'psr.global_transaction_comments'
        verbose_name = 'global_transaction_comments'
        verbose_name_plural = 'global_transaction_comments'


class SystemEquipmentCompartment(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    type = models.SmallIntegerField(choices=((1,'system'),(2,'equipment'),(3,'compartment')))
    ser = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    numbers = models.TextField(null=True, blank=True)
    capabilities_feature = models.TextField(null=True, blank=True)
    weight_volume_power_consumption = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    interface = models.TextField(null=True, blank=True)
    procurement_router = models.TextField(null=True, blank=True)
    vendor = models.TextField(null=True, blank=True)
    cost = models.TextField(null=True, blank=True)
    standards = models.TextField(null=True, blank=True)
    sustenance = models.TextField(null=True, blank=True)

    equipment = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    layout = models.TextField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.module
    class Meta:
        db_table = 'psr.system_equipment_compartment'
        verbose_name = 'SystemEquipmentCompartment'
        verbose_name_plural = 'SystemEquipmentCompartment'

        

class ProjectLog(models.Model):     
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,null=True,blank=True)
    sub_module = models.ForeignKey(SubModule, on_delete=models.CASCADE) 
    msg =  models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):

        return self.project


    class Meta:
        db_table = 'log.projectlog'
        verbose_name = 'ProjectLog'
        verbose_name_plural = 'ProjectLog'



class SystemEquipmentCompartmentTemp(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    section = models.ForeignKey(GlobalSection, on_delete=models.CASCADE, null=True)
    sub_section = models.ForeignKey(GlobalSubSection, on_delete=models.CASCADE, null=True)
    sub_sub_section = models.ForeignKey(GlobalSubSubSection, on_delete=models.CASCADE, null=True)
    type = models.SmallIntegerField(choices=((1,'system'),(2,'equipment'),(3,'compartment')))
    ser = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    numbers = models.TextField(null=True, blank=True)
    capabilities_feature = models.TextField(null=True, blank=True)
    weight_volume_power_consumption = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    interface = models.TextField(null=True, blank=True)
    procurement_router = models.TextField(null=True, blank=True)
    vendor = models.TextField(null=True, blank=True)
    cost = models.TextField(null=True, blank=True)
    standards = models.TextField(null=True, blank=True)
    sustenance = models.TextField(null=True, blank=True)

    equipment = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    layout = models.TextField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(default = 1, choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.module
    class Meta:
        db_table = 'psr.system_equipment_compartment_temp'
        verbose_name = 'SystemEquipmentCompartment_temp'
        verbose_name_plural = 'SystemEquipmentCompartmentTemp'


class GlobalTransactionEditPdf(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    html =  models.TextField(null=True, blank=True)
    form_id = models.IntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'psr.global_transaction_edit_pdf'
        verbose_name = 'global_transaction_edit_pdf'
        verbose_name_plural = 'global_transaction_edit_pdf'


class FormLevelRecommenderHierarchy(models.Model):

    form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    recommender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='fl_recommender')
    recommender_level = models.IntegerField(null=True)
    recommender_level_status = models.SmallIntegerField(null=True)
    current_reject = models.SmallIntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.form

    class Meta:
        db_table = 'hierarchy.form_level_recommender'
        verbose_name = 'hierarchy_form_level_recommender'
        verbose_name_plural = 'hierarchy_form_level_recommender'


class FormLevelApproverHierarchy(models.Model):

    form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="fl_approver")
    approver_level = models.IntegerField(null=True)
    approver_level_status = models.SmallIntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.form

    class Meta:
        db_table = 'hierarchy.form_level_approver'
        verbose_name = 'hierarchy_form_level_approver'
        verbose_name_plural = 'hierarchy_form_level_approver'


class ProjectLevelRecommenderHierarchy(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    recommender =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="pl_recommender")
    recommender_level = models.IntegerField(null=True)
    recommender_level_status = models.SmallIntegerField(null=True)
    current_reject = models.SmallIntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'hierarchy.project_level_recommender'
        verbose_name = 'hierarchy_project_level_recommender'
        verbose_name_plural = 'hierarchy_project_level_recommender'


class ProjectLevelApproverHierarchy(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="pl_approver")
    approver_level = models.IntegerField(null=True)
    approver_level_status = models.SmallIntegerField(null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'hierarchy.project_level_approver'
        verbose_name = 'hierarchy_project_level_approver'
        verbose_name_plural = 'hierarchy_project_level_approver'


class GlobalTransactionShipDetail(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    #form = models.ForeignKey(Forms, on_delete=models.CASCADE, null=True)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    ship_id = models.CharField(max_length=15, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        db_table = 'transaction.ship_details'
        verbose_name = 'transaction_ship_details'
        verbose_name_plural = 'transaction_ship_details'



#### DOCK YARD #####


class ExcelFileDefectUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/Defect/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)
    

    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'defect.excel_file_upload'
        verbose_name = 'Defect Excel File Upload'
        verbose_name_plural = 'Defect Excel File Upload'


class ExcelFileShipUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/Ship/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'ship.excel_file_upload'
        verbose_name = 'Ship Excel File Upload'
        verbose_name_plural = 'Ship Excel File Upload'


class ExcelFileEquipmentUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/Equipment/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'equipment.excel_file_upload'
        verbose_name = 'Equipment Excel File Upload'
        verbose_name_plural = 'Equipment Excel File Upload'


class ExcelFileDartUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/Dart/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'dart.excel_file_upload'
        verbose_name = 'Dart Excel File Upload'
        verbose_name_plural = 'Dart Excel File Upload'

class ExcelFileRAUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/RA/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'ra.excel_file_upload'
        verbose_name = 'RA Excel File Upload'
        verbose_name_plural = 'RA Excel File Upload'


class ExcelFileOPDEFUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="Excel/RA/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.excel_file_upload

    class Meta:
        db_table = 'opdef.excel_file_upload'
        verbose_name = 'OPDEF Excel File Upload'
        verbose_name_plural = 'OPDEF Excel File Upload'


class Dart(models.Model):

    SrNo = models.CharField(max_length=100, blank=True, null=True)
    ShipSrNo = models.CharField(max_length=100, blank=True, null=True)
    DartDate = models.DateTimeField(blank=True, null=True)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    ExDept = models.CharField(max_length=100, blank=True, null=True)
    ExDeptID = models.CharField(max_length=100, blank=True, null=True)
    EquipmentShipID = models.CharField(max_length=100, blank=True, null=True)
    EquipmentCode = models.CharField(max_length=100, blank=True, null=True)
    SeverityID = models.CharField(max_length=100, blank=True, null=True)
    SeverityCode = models.CharField(max_length=100, blank=True, null=True)
    DiagnosticID = models.CharField(max_length=100, blank=True, null=True)
    DiagnosticCode = models.CharField(max_length=100, blank=True, null=True)
    RectifiedDate = models.DateTimeField(blank=True, null=True)
    RepairID = models.CharField(max_length=100, blank=True, null=True)
    RepairCode = models.CharField(max_length=100, blank=True, null=True)
    RepairAgencyID = models.CharField(max_length=100, blank=True, null=True)
    AgencyCode = models.CharField(max_length=100, blank=True, null=True)
    DelayID = models.CharField(max_length=100, blank=True, null=True)
    DelayCode = models.CharField(max_length=100, blank=True, null=True)
    Remarks = models.TextField(null=True, blank=True)
    OpdefSrNo = models.CharField(max_length=100, blank=True, null=True)
    XdueRefitType = models.CharField(max_length=100, blank=True, null=True)
    XdueRefitRemarks = models.TextField(null=True, blank=True)
    CancelDate = models.DateTimeField(blank=True, null=True)
    NILDart = models.CharField(max_length=100, blank=True, null=True)
    Active = models.CharField(max_length=100, blank=True, null=True)

    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedBy = models.CharField(max_length=100, blank=True, null=True)
    UpdatedDate = models.DateTimeField(auto_now_add=True)
    Source = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_ip = models.GenericIPAddressField()

    def __str__(self):
        return self.SrNo

    class Meta:
        db_table = 'transaction.dart'
        verbose_name = 'dart'
        verbose_name_plural = 'dart'


class RA(models.Model): # Request Assistance

    SrNo = models.CharField(max_length=100, blank=True, null=True)
    ShipSrNo = models.CharField(max_length=100, blank=True, null=True)
    DartDate = models.DateTimeField(blank=True, null=True)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    ExDept = models.CharField(max_length=100, blank=True, null=True)
    ExDeptID = models.CharField(max_length=100, blank=True, null=True)
    EquipmentShipID = models.CharField(max_length=100, blank=True, null=True)
    EquipmentCode = models.CharField(max_length=100, blank=True, null=True)
    SeverityID = models.CharField(max_length=100, blank=True, null=True)
    SeverityCode = models.CharField(max_length=100, blank=True, null=True)
    DiagnosticID = models.CharField(max_length=100, blank=True, null=True)
    DiagnosticCode = models.CharField(max_length=100, blank=True, null=True)
    RectifiedDate = models.DateTimeField(blank=True, null=True)
    RepairID = models.CharField(max_length=100, blank=True, null=True)
    RepairCode = models.CharField(max_length=100, blank=True, null=True)
    RepairAgencyID = models.CharField(max_length=100, blank=True, null=True)
    AgencyCode = models.CharField(max_length=100, blank=True, null=True)
    DelayID = models.CharField(max_length=100, blank=True, null=True)
    DelayCode = models.CharField(max_length=100, blank=True, null=True)
    Remarks = models.TextField(null=True, blank=True)
    OpdefSrNo = models.CharField(max_length=100, blank=True, null=True)
    XdueRefitType = models.CharField(max_length=100, blank=True, null=True)
    XdueRefitRemarks = models.TextField(null=True, blank=True)
    CancelDate = models.DateTimeField(blank=True, null=True)
    NILDart = models.CharField(max_length=100, blank=True, null=True)
    Active = models.CharField(max_length=100, blank=True, null=True)

    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedBy = models.CharField(max_length=100, blank=True, null=True)
    UpdatedDate = models.DateTimeField(auto_now_add=True)
    Source = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_ip = models.GenericIPAddressField()

    def __str__(self):
        return self.SrNo

    class Meta:
        db_table = 'transaction.ra'
        verbose_name = 'ra'
        verbose_name_plural = 'ra'


class OPDEF(models.Model):

    OpdefDate = models.DateTimeField(blank=True, null=True)
    OpdefNo = models.CharField(max_length=100, blank=True, null=True)
    ShipID = models.CharField(max_length=100, blank=True, null=True)
    Command = models.CharField(max_length=100, blank=True, null=True)
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    DartNo = models.CharField(max_length=100, blank=True, null=True)
    STA = models.CharField(max_length=100, blank=True, null=True)
    EquipmentID = models.CharField(max_length=100, blank=True, null=True)
    LocationCode = models.CharField(max_length=100, blank=True, null=True)
    Unit = models.CharField(max_length=100, blank=True, null=True)
    Defect = models.CharField(max_length=100, blank=True, null=True)
    Severity = models.CharField(max_length=100, blank=True, null=True)
    AssistanceRequired = models.CharField(max_length=100, blank=True, null=True)
    EffectOnOperation = models.CharField(max_length=100, blank=True, null=True)
    DowngradeDate = models.DateTimeField(blank=True, null=True)
    STADowngradeDate = models.DateTimeField(blank=True, null=True)
    STAUpgradeDate = models.DateTimeField(blank=True, null=True)
    CancelDtg = models.CharField(max_length=100, blank=True, null=True)
    CancelDate = models.DateTimeField(blank=True, null=True)
    RepairDate = models.DateTimeField(blank=True, null=True)
    RepairID = models.CharField(max_length=100, blank=True, null=True)
    RepairParts = models.CharField(max_length=100, blank=True, null=True)

    HoldupCode = models.CharField(max_length=100, blank=True, null=True)
    HoldupDetail = models.CharField(max_length=100, blank=True, null=True)
    INSMAEffort = models.CharField(max_length=100, blank=True, null=True)
    Refit = models.CharField(max_length=100, blank=True, null=True)
    Active = models.CharField(max_length=100, blank=True, null=True)

    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedBy = models.CharField(max_length=100, blank=True, null=True)
    UpdatedDate = models.DateTimeField(auto_now_add=True)

    Remarks = models.TextField(null=True, blank=True)
    StoredemSrNo = models.CharField(max_length=100, blank=True, null=True)
    OpDefStatus = models.CharField(max_length=100, blank=True, null=True)
    EquipmentSerialNo = models.CharField(max_length=100, blank=True, null=True)

    OfarDate = models.DateTimeField(blank=True, null=True)

    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_ip = models.GenericIPAddressField()

    def __str__(self):
        return self.SrNo

    class Meta:
        db_table = 'transaction.opdef'
        verbose_name = 'opdef'
        verbose_name_plural = 'opdef'


class WorkInstruction(models.Model): # WI

    name = models.CharField(max_length=100, blank=True, null=True)
    dart = models.ForeignKey(Dart, on_delete=models.CASCADE, null=True)
    man_days = models.IntegerField(null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    status_description = models.TextField(null=True, blank=True)
    WI_close_date = models.DateTimeField(blank=True, null=True)
    refit_type = models.ForeignKey(RefitType, on_delete=models.CASCADE, null=True)
    qc_status = models.SmallIntegerField(choices=((1,'Accept'),(2,'Reject'),(3,'Recommend')))
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.dart

    class Meta:
        db_table = 'transaction.work_instruction'
        verbose_name = 'work_instruction'
        verbose_name_plural = 'work_instruction'

class WorkInstructionQCCheck(models.Model):

    work_instruction = models.ForeignKey(WorkInstruction, on_delete=models.CASCADE, null=True)
    remarks = models.TextField(null=True, blank=True)
    qc_status = models.SmallIntegerField(choices=((1,'Accept'),(2,'Reject'),(3,'Recommend')))
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.work_instruction

    class Meta:
        db_table = 'transaction.work_instruction_qc_check'
        verbose_name = 'work_instruction_qc_check'
        verbose_name_plural = 'work_instruction_qc_check'



class JobCard(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    work_instruction = models.ForeignKey(WorkInstruction, on_delete=models.CASCADE, null=True)
    man_days = models.IntegerField(null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    instruction = models.TextField(null=True, blank=True)
    job_card_close_date = models.DateTimeField(blank=True, null=True)
    qc_status = models.SmallIntegerField(choices=((1,'Accept'),(2,'Reject'),(3,'Recommend')))
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.work_instruction

    class Meta:
        db_table = 'transaction.job_card'
        verbose_name = 'job_card'
        verbose_name_plural = 'job_card'

class JobCardQCCheck(models.Model):

    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, null=True)
    remarks = models.TextField(null=True, blank=True)
    qc_status = models.SmallIntegerField(choices=((1,'Accept'),(2,'Reject'),(3,'Recommend')))
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.job_card

    class Meta:
        db_table = 'transaction.job_card_qc_check'
        verbose_name = 'job_card_qc_check'
        verbose_name_plural = 'job_card_qc_check'


class Attendance(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    attendance_date = models.DateField(blank=True, null=True)
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    attendance_status = models.SmallIntegerField(choices=((1,'Present'),(2,'Absent')))
    #total_work = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    total_work = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='a_user')
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'transaction.attendance'
        verbose_name = 'attendance'
        verbose_name_plural = 'attendance'

class MonthlySalary(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    for_month = models.DateTimeField(blank=True,null=True)
    total_credits = models.DecimalField(max_digits=6, decimal_places=2)
    total_debits = models.DecimalField(max_digits=6, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=6, decimal_places=2)
    net_salary = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='ms_user')
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    
    def __str__(self):
        return self.user
     
     
    class Meta:
        db_table = 'transaction.monthly_salary'
        verbose_name = 'monthly_salary'
        verbose_name_plural = 'monthly_salary'

class MonthlyCreditsDebits(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    for_month = models.DateField(blank=True, null=True)
    allowance = models.ForeignKey(AllowancesMaster, on_delete=models.CASCADE, null=True)
    allowance_amount = models.DecimalField(max_digits=6, decimal_places=2)
    deduction = models.ForeignKey(DeductionsMaster, on_delete=models.CASCADE, null=True)
    deduction_amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='mcd_user')
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'transaction.monthly_credits_debits'
        verbose_name = 'monthly_credits_debits'
        verbose_name_plural = 'monthly_credits_debits'


class ManpowerBooking(models.Model):

    date = models.DateField(blank=True, null=True)
    time = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    shop_floor = models.ForeignKey(Shopfloor, on_delete=models.CASCADE, null=True)
    status_master = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True)
    work_instruction = models.ForeignKey(WorkInstruction, on_delete=models.CASCADE, null=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, null=True)

    over_time = models.ForeignKey(OverTime, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(choices=((1,'Active'),(2,'Inactive'),(3,'Delete')))
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='mb_user')
    created_ip = models.GenericIPAddressField()
    modified_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.date

    class Meta:
        db_table = 'transaction.manpower_booking'
        verbose_name = 'manpower_booking'
        verbose_name_plural = 'manpower_booking'