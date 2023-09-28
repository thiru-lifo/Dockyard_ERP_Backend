from django.urls import path
from . import views

urlpatterns = [
    path('countries',views.CountriesViews.as_view(), name = 'viewcountries'),
    path('countries/<int:pk>',views.CountriesViews.as_view(), name = 'viewcountry'),
    path('countries/details',views.CountriesDetailViews.as_view(), name = 'addcountries'),
    
    path('states',views.StatesViews.as_view(), name = 'viewstates'),
    path('states/<int:pk>',views.StatesViews.as_view(), name = 'viewstate'),
    path('states/details',views.StatesDetailViews.as_view(), name = 'addstates'),
    
    path('cities',views.CityViews.as_view(), name = 'viewcities'),
    path('cities/<int:pk>',views.CityViews.as_view(), name = 'viewcity'),
    path('cities/details', views.CityDetailViews.as_view(), name= 'addcities'),


    path('lookup_type', views.LookupTypeViews.as_view(), name = 'view_lookup_type'),
    path('lookup_type/<int:pk>', views.LookupTypeViews.as_view(), name = 'view_lookup_type'),
    path('lookup_type/details', views.LookupTypeDetailViews.as_view(), name = 'add_lookup_type'),

    path('lookup', views.LookupViews.as_view(), name = 'view_lookup'),
    path('lookup/<int:pk>', views.LookupViews.as_view(), name = 'view_lookup'),
    path('lookup/details', views.LookupDetailViews.as_view(), name = 'add_lookup'),


    path('region', views.RegionViews.as_view(), name = 'view_region'),
    path('region/<int:pk>', views.RegionViews.as_view(), name = 'view_region'),
    path('region/details', views.RegionDetailViews.as_view(), name = 'add_region'),

    path('project_type', views.ProjectTypeViews.as_view(), name = 'view_project_type'),
    path('project_type/<int:pk>', views.ProjectTypeViews.as_view(), name = 'view_project_type'),
    path('project_type/details', views.ProjectTypeDetailViews.as_view(), name = 'add_project_type'),

    path('project', views.ProjectViews.as_view(), name = 'view_region'),
    path('project/<int:pk>', views.ProjectViews.as_view(), name = 'view_region'),
    path('project/details', views.ProjectDetailViews.as_view(), name = 'add_region'),

    path('command', views.CommandViews.as_view(), name = 'view_command'),
    path('command/<int:pk>', views.CommandViews.as_view(), name = 'view_command'),
    path('command/details', views.CommandDetailViews.as_view(), name = 'add_command'),

    path('department', views.DepartmentViews.as_view(), name = 'view_department'),
    path('department/<int:pk>', views.DepartmentViews.as_view(), name = 'view_department'),
    path('department/details', views.DepartmentDetailViews.as_view(), name = 'add_department'),

    path('section', views.SectionViews.as_view(), name = 'view_section'),
    path('section/<int:pk>', views.SectionViews.as_view(), name = 'view_section'),
    path('section/details', views.SectionDetailViews.as_view(), name = 'add_section'),

    path('sub_section', views.SubSectionViews.as_view(), name = 'view_sub_section'),
    path('sub_section/<int:pk>', views.SubSectionViews.as_view(), name = 'view_sub_section'),
    path('sub_section/details', views.SubSectionDetailViews.as_view(), name = 'add_sub_section'),

    path('unit_type', views.UnitTypeViews.as_view(), name = 'view_unit_type'),
    path('unit_type/<int:pk>', views.UnitTypeViews.as_view(), name = 'view_unit_type'),
    path('unit_type/details', views.UnitTypeDetailViews.as_view(), name = 'add_unit_type'),

    path('unit', views.UnitViews.as_view(), name = 'view_unit'),
    path('unit/<int:pk>', views.UnitViews.as_view(), name = 'view_unit'),
    path('unit/details', views.UnitDetailViews.as_view(), name = 'add_unit'),

    path('authority', views.AuthorityViews.as_view(), name = 'view_authority'),
    path('authority/<int:pk>', views.AuthorityViews.as_view(), name = 'view_authority'),
    path('authority/details', views.AuthorityDetailViews.as_view(), name = 'add_authority'),

    path('class', views.ClassViews.as_view(), name = 'view_class'),
    path('class/<int:pk>', views.ClassViews.as_view(), name = 'view_class'),
    path('class/details', views.ClassDetailViews.as_view(), name = 'add_class'),

    path('ship', views.ShipViews.as_view(), name = 'view_ship'),
    path('ship/<int:pk>', views.ShipViews.as_view(), name = 'view_ship'),
    path('ship/details', views.ShipDetailViews.as_view(), name = 'add_ship'),


    path('ships', views.ShipsViews.as_view(), name = 'view_ships'),
    path('ships/<int:pk>', views.ShipsViews.as_view(), name = 'view_ships'),
    path('ships/details', views.ShipsDetailViews.as_view(), name = 'add_ships'),

    path('compartment', views.CompartmentViews.as_view(), name = 'view_compartment'),
    path('compartment/<int:pk>', views.CompartmentViews.as_view(), name = 'view_compartment'),
    path('compartment/details', views.CompartmentDetailViews.as_view(), name = 'add_compartment'),

    path('system', views.SystemViews.as_view(), name = 'view_system'),
    path('system/<int:pk>', views.SystemViews.as_view(), name = 'view_systemn'),
    path('system/details', views.SystemDetailViews.as_view(), name = 'add_system'),

    path('equipment', views.EquipmentViews.as_view(), name = 'view_equipment'),
    path('equipment/<int:pk>', views.EquipmentViews.as_view(), name = 'view_equipment'),
    path('equipment/details', views.EquipmentDetailViews.as_view(), name = 'add_equipment'),

    path('status', views.GlobalStatusViews.as_view(), name = 'view_status'),
    path('status/<int:pk>', views.GlobalStatusViews.as_view(), name = 'view_status'),
    path('status/details', views.GlobalStatusDetailViews.as_view(), name = 'add_status'),    

    path('designation', views.DesignationViews.as_view(), name = 'view_designation'),
    path('designation/<int:pk>', views.DesignationViews.as_view(), name = 'view_designation'),
    path('designation/details', views.DesignationDetailViews.as_view(), name = 'add_designation'),


    # Global Section
    path('global_section', views.GlobalSectionViews.as_view(), name = 'view_global_section'),
    path('global_section/<int:pk>', views.GlobalSectionViews.as_view(), name = 'view_global_section'),
    path('global_section/details', views.GlobalSectionDetailViews.as_view(), name = 'add_global_section'),

    path('global_sub_section', views.GlobalSubSectionViews.as_view(), name = 'view_global_sub_section'),
    path('global_sub_section/<int:pk>', views.GlobalSubSectionViews.as_view(), name = 'view_global_sub_section'),
    path('global_sub_section/details', views.GlobalSubSectionDetailViews.as_view(), name = 'add_global_sub_section'),

    path('global_sub_sub_section', views.GlobalSubSubSectionViews.as_view(), name = 'view_global_sub_sub_section'),
    path('global_sub_sub_section/<int:pk>', views.GlobalSubSubSectionViews.as_view(), name = 'view_global_sub_sub_section'),
    path('global_sub_sub_section/details', views.GlobalSubSubSectionDetailViews.as_view(), name = 'add_global_sub_section'),

    ##########

    path('module', views.ModuleViews.as_view(), name = 'view_module'),
    path('module/<int:pk>', views.ModuleViews.as_view(), name = 'view_module'),
    path('module/details', views.ModuleDetailViews.as_view(), name = 'add_module'),

    path('sub_module', views.SubModuleViews.as_view(), name = 'view_sub_module'),
    path('sub_module/<int:pk>', views.SubModuleViews.as_view(), name = 'view_module'),
    path('sub_module/details', views.SubModuleDetailViews.as_view(), name = 'add_sub_module'),

    path('template', views.TemplateViews.as_view(), name = 'view_template'),
    path('template/<int:pk>', views.TemplateViews.as_view(), name = 'view_template'),
    path('template/details', views.TemplateDetailViews.as_view(), name = 'add_template'),

    path('template_config', views.TemplateConfigViews.as_view(), name = 'view_template_config'),
    path('template_config/<int:pk>', views.TemplateConfigViews.as_view(), name = 'view_template_config'),
    path('template_config/details', views.TemplateConfigDetailViews.as_view(), name = 'add_template_config'),

    path('template_config_master',views.TemplateConfigMasterViews.as_view(), name = 'Template Config Master View'),
    
    path('template_config_master/delete', views.DeleteTemplateConfigMaster.as_view(), name="DeleteTemplateConfigMaster"),

    ####################
    path('generate_psr_template', views.GeneratePSRTemplateViews.as_view(), name="Generate PSR Template"),

    path('section_compartment', views.getSectionCompartment.as_view(), name="Section Compartment"),
    path('section_system', views.getSectionSystem.as_view(), name="Section System"),
    path('section_equipment', views.getSectionEquipment.as_view(), name="Section Equipment"),

    ### FormMapping ###
    path('module_form_mapping', views.FormMappingModuleViews.as_view(), name = 'form_mapping_view_module'),

    path('sub_module_form_mapping', views.FormMappingSubModuleViews.as_view(), name = 'form_mapping_view_sub_module'), 
    path('global_section_form_mapping', views.FormMappingGlobalSectionViews.as_view(), name = 'form_mapping_view_global_section'),
    path('global_sub_section_form_mapping', views.FormMappingGlobalSubSectionViews.as_view(), name = 'form_mapping_view_global_sub_section'),
    path('global_sub_sub_section_form_mapping', views.FormMappingGlobalSubSubSectionViews.as_view(), name = 'form_mapping_view_global_sub_sub_section'),

]