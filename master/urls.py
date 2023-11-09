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



    # path('dockyard_group', views.DockyardGroupViews.as_view(), name = 'view_dockyard_group'),
    # path('dockyard_group/<int:pk>', views.DockyardGroupViews.as_view(), name = 'view_dockyard_group'),
    # path('dockyard_group/details', views.DockyardGroupDetailViews.as_view(), name = 'add_dockyard_group'),



    path('ship', views.ShipViews.as_view(), name = 'view_ship'),
    path('ship/<int:pk>', views.ShipViews.as_view(), name = 'view_ship'),
    path('ship/details', views.ShipDetailViews.as_view(), name = 'add_ship'),
    path('ship/excel', views.ImportExcelShip.as_view(), name="Ship Excel"),


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
    path('equipment_list', views.EquipmentList.as_view(), name = 'equipment_list'),
    path('equipment/<int:pk>', views.EquipmentViews.as_view(), name = 'view_equipment'),
    path('equipment/details', views.EquipmentDetailViews.as_view(), name = 'add_equipment'),
    path('equipment/excel', views.ImportExcelEquipment.as_view(), name="Equipment Excel"),

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



    # Dockyard #

    path('dockyard', views.DockyardViews.as_view(), name = 'view_dockyard'),
    path('dockyard/<int:pk>', views.DockyardViews.as_view(), name = 'view_dockyard'),
    path('dockyard/details', views.DockyardDetailViews.as_view(), name = 'add_dockyard'),

    path('dockyard_group', views.DockyardGroupViews.as_view(), name = 'dockyard_group_class'),
    path('dockyard_group/<int:pk>', views.DockyardGroupViews.as_view(), name = 'dockyard_group_class'),
    path('dockyard_group/details', views.DockyardGroupDetailViews.as_view(), name = 'add_dockyard_group_class'),

    path('dockyard_sub_group', views.DockyardSubGroupViews.as_view(), name = 'dockyard_sub_group_class'),
    path('dockyard_sub_group/<int:pk>', views.DockyardSubGroupViews.as_view(), name = 'dockyard_sub_group_class'),
    path('dockyard_sub_group/details', views.DockyardSubGroupDetailViews.as_view(), name = 'add_dockyard_sub_group_class'),

    path('refit_type', views.RefitTypeViews.as_view(), name = 'view_refit_type'),
    path('refit_type/<int:pk>', views.RefitTypeViews.as_view(), name = 'view_refit_type'),
    path('refit_type/details', views.RefitTypeDetailViews.as_view(), name = 'add_refit_type'),

    path('defect', views.DefectViews.as_view(), name = 'view_defect'),
    path('defect/<int:pk>', views.DefectViews.as_view(), name = 'view_defect'),
    path('defect/details', views.DefectDetailViews.as_view(), name = 'add_defect'),
    path('defect/excel', views.ImportExcelDefect.as_view(), name="Defect Excel"),

    path('get_defect_detail', views.GetDefectDetail.as_view(), name="Get Defect Detail"),

    path('center', views.CenterViews.as_view(), name = 'view_center'),
    path('center/<int:pk>', views.CenterViews.as_view(), name = 'view_center'),
    path('center/details', views.CenterDetailViews.as_view(), name = 'add_center'),

    path('shop_floor', views.ShopFloorViews.as_view(), name = 'view_shop_floor'),
    path('shop_floor/<int:pk>', views.ShopFloorViews.as_view(), name = 'view_shop_floor'),
    path('shop_floor/details', views.ShopFloorDetailViews.as_view(), name = 'add_shop_floor'),

    path('category_type', views.CategoryTypeViews.as_view(), name = 'view_category_type'),
    path('category_type/<int:pk>', views.CategoryTypeViews.as_view(), name = 'view_category_type'),
    path('category_type/details', views.CategoryTypeDetailViews.as_view(), name = 'add_category_type'),

    path('pay_scale', views.PayScaleViews.as_view(), name = 'view_pay_scale'),
    path('pay_scale/<int:pk>', views.PayScaleViews.as_view(), name = 'view_pay_scale'),
    path('pay_scale/details', views.PayScaleDetailViews.as_view(), name = 'add_pay_scale'),

    path('demand_master', views.DemandMasterViews.as_view(), name = 'view_demand_master'),
    path('demand_master/<int:pk>', views.DemandMasterViews.as_view(), name = 'view_demand_master'),
    path('demand_master/details', views.DemandMasterDetailViews.as_view(), name = 'add_demand_master'),

    path('items_master', views.ItemsMasterViews.as_view(), name = 'view_items_master'),
    path('items_master/<int:pk>', views.ItemsMasterViews.as_view(), name = 'view_items_master'),
    path('items_master/details', views.ItemsMasterDetailViews.as_view(), name = 'add_items_master'),

    path('allowances_master', views.AllowancesMasterViews.as_view(), name = 'view_allowances_master'),
    path('allowances_master/<int:pk>', views.AllowancesMasterViews.as_view(), name = 'view_allowances_master'),
    path('allowances_master/details', views.AllowancesMasterDetailViews.as_view(), name = 'add_allowances_master'),

    path('deductions_master', views.DeductionsMasterViews.as_view(), name = 'view_deductions_master'),
    path('deductions_master/<int:pk>', views.DeductionsMasterViews.as_view(), name = 'view_deductions_master'),
    path('deductions_master/details', views.DeductionsMasterDetailViews.as_view(), name = 'add_deductions_master'),

    path('pay_grade', views.PayGradeViews.as_view(), name = 'view_pay_grade'),
    path('pay_grade/<int:pk>', views.PayGradeViews.as_view(), name = 'view_pay_grade'),
    path('pay_grade/details', views.PayGradeDetailViews.as_view(), name = 'add_pay_grade'),

    path('personnel_type', views.PersonnelTypeViews.as_view(), name = 'view_personnel_type'),
    path('personnel_type/<int:pk>', views.PersonnelTypeViews.as_view(), name = 'view_personnel_type'),
    path('personnel_type/details', views.PersonnelTypeDetailViews.as_view(), name = 'add_personnel_type'),

    path('status_master', views.StatusMasterViews.as_view(), name = 'view_status_master'),
    path('status_master/<int:pk>', views.StatusMasterViews.as_view(), name = 'view_status_master'),
    path('status_master/details', views.StatusMasterDetailViews.as_view(), name = 'add_status_master'),


    path('rank', views.RankViews.as_view(), name = 'view_rank'),
    path('rank/<int:pk>', views.RankViews.as_view(), name = 'view_rank'),
    path('rank/details', views.RankDetailViews.as_view(), name = 'add_rank'),


   
    path('item_type', views.ItemTypeViews.as_view(), name = 'view_item_type'),
    path('item_type/<int:pk>', views.ItemTypeViews.as_view(), name = 'view_item_type'),
    path('item_type/details', views.ItemTypeDetailViews.as_view(), name = 'add_item_type'),

    path('storage_location', views.StorageLocationViews.as_view(), name = 'view_storage_location'),
    path('storage_location/<int:pk>', views.StorageLocationViews.as_view(), name = 'view_storage_location'),
    path('storage_location/details', views.StorageLocationDetailViews.as_view(), name = 'add_storage_location'),


    path('issue', views.IssueViews.as_view(), name = 'view_issue'),
    path('issue/<int:pk>', views.IssueViews.as_view(), name = 'view_issue'),
    path('issue/details', views.IssueDetailViews.as_view(), name = 'add_issue'),


    path('course', views.CourseViews.as_view(), name = 'view_course'),
    path('course/<int:pk>', views.CourseViews.as_view(), name = 'view_course'),
    path('course/details', views.CourseDetailViews.as_view(), name = 'add_course'),

    
    path('batch', views.BatchViews.as_view(), name = 'view_batch'),
    path('batch/<int:pk>', views.BatchViews.as_view(), name = 'view_batch'),
    path('batch/details', views.BatchDetailViews.as_view(), name = 'add_batch'),


    path('over-time', views.OverTimeViews.as_view(), name = 'view_over_time'),
    path('over-time/<int:pk>', views.OverTimeViews.as_view(), name = 'view_over_time'),
    path('over-time/details', views.OverTimeDetailViews.as_view(), name = 'add_over_time'),


    path('holiday', views.HolidayViews.as_view(), name = 'view_holiday'),
    path('holiday/<int:pk>', views.HolidayViews.as_view(), name = 'view_holiday'),
    path('holiday/details', views.HolidayDetailViews.as_view(), name = 'add_holiday'),


    path('stock_register', views.StockRegisterViews.as_view(), name = 'view_stock_register'),
    path('stock_register/<int:pk>', views.StockRegisterViews.as_view(), name = 'view_stock_register'),
    path('stock_register/details', views.StockRegisterDetailViews.as_view(), name = 'add_stock_register'),

    # path('stock_log', views.StockLogViews.as_view(), name = 'view_stock_log'),
    # path('stock_log/<int:pk>', views.StockLogViews.as_view(), name = 'view_stock_log'),
    # path('stock_log/details', views.StockLogDetailViews.as_view(), name = 'add_stock_log'),

    path('stock_generation', views.StockLogViews.as_view(), name = 'view_stock_generation'),
    path('stock_generation/<int:pk>', views.StockLogViews.as_view(), name = 'view_stock_generation'),
    path('stock_generation/details', views.StockLogDetailViews.as_view(), name = 'add_stock_generation'),




    path('promotion', views.PromotionViews.as_view(), name = 'view_promotion'),
    path('promotion/<int:pk>', views.PromotionViews.as_view(), name = 'view_promotion'),
    path('promotion/details', views.PromotionDetailViews.as_view(), name = 'add_promotion'),


]