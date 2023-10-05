from django.urls import path
from . import views


urlpatterns = [
    path('psr/primary_roles', views.PrimaryRolesViews.as_view(), name = 'view_primary_roles'),
    path('psr/primary_roles/<int:pk>', views.PrimaryRolesViews.as_view(), name = 'view_primary_roles'),
    path('psr/primary_roles/details', views.PrimaryRolesDetailViews.as_view(), name = 'add_primary_roles'),

    path('psr/secondary_roles', views.SecondaryRolesViews.as_view(), name = 'view_secondary_roles'),
    path('psr/secondary_roles/<int:pk>', views.SecondaryRolesViews.as_view(), name = 'view_secondary_roles'),
    path('psr/secondary_roles/details', views.SecondaryRolesDetailViews.as_view(), name = 'add_secondary_roles'),

    path('psr/standard', views.StandardViews.as_view(), name = 'view_standard'),
    path('psr/standard/<int:pk>', views.StandardViews.as_view(), name = 'view_standard'),
    path('psr/standard/details', views.StandardDetailViews.as_view(), name = 'add_standard'),

    path('psr/plan_for_manpower_induction', views.PlanForManpowerInductionViews.as_view(), name = 'view_plan_for_manpower_induction'),
    path('psr/plan_for_manpower_induction/<int:pk>', views.PlanForManpowerInductionViews.as_view(), name = 'view_plan_for_manpower_induction'),
    path('psr/plan_for_manpower_induction/details', views.PlanForManpowerInductionDetailViews.as_view(), name = 'add_plan_for_manpower_induction'),

    path('psr/acquisition_method', views.AcquisitionMethodViews.as_view(), name = 'view_acquisition_method'),
    path('psr/acquisition_method/<int:pk>', views.AcquisitionMethodViews.as_view(), name = 'view_acquisition_method'),
    path('psr/acquisition_method/details', views.AcquisitionMethodDetailViews.as_view(), name = 'add_acquisition_method'),


    path('psr/sss', views.SSSViews.as_view(), name = 'view_sss'),
    path('psr/sss/<int:pk>', views.SSSViews.as_view(), name = 'view_sss'),
    path('psr/sss/details', views.SSSDetailViews.as_view(), name = 'add_sss'),


    path('psr/section', views.PSRSectionViews.as_view(), name = 'view_psr_section'),
    path('psr/section/<int:pk>', views.PSRSectionViews.as_view(), name = 'view_psr_section'),
    path('psr/section/details', views.PSRSectionDetailViews.as_view(), name = 'add_psr_section'),

    path('psr/sectionlist', views.PSRSectionViews2.as_view(), name = 'view_psr_section'),

    path('psr/sub_section', views.PSRSubSectionViews.as_view(), name = 'view_sub_section'),
    path('psr/sub_section/<int:pk>', views.PSRSubSectionViews.as_view(), name = 'view_sub_section'),
    path('psr/sub_section/details', views.PSRSubSectionDetailViews.as_view(), name = 'add_sub_section'),

    # PSR Initiation Notes
    path('psr/initiation_notes',views.InitiationNotesList.as_view(), name = 'Initiation Notes List'),
    path('psr/initiation_notes/crud',views.InitiationNotesCRUD.as_view(), name = 'Initiation Notes CRUD'),

    # PSR Initiation Notes Document
    path('psr/initiation_notes_document',views.InitiationNotesDocumentList.as_view(), name = 'Initiation Notes Document List'),
    path('psr/initiation_notes_document/crud',views.InitiationNotesDocumentCRUD.as_view(), name = 'Initiation Notes Document CRUD'),

    # PSR Initiation Notes Send Email
    path('psr/initiation_notes_send_email',views.InitiationNotesSendMailList.as_view(), name = 'Initiation Notes Send Email List'),
    path('psr/initiation_notes_send_email/crud',views.InitiationNotesSendMailCRUD.as_view(), name = 'Initiation Notes Send Email CRUD'),


    # PSR Formulation Of Approach Paper
    path('psr/formulation_of_approach_paper',views.FormulationOfApproachPaperList.as_view(), name = 'Formulation Of Approach Paper List'),
    path('psr/formulation_of_approach_paper/crud',views.FormulationOfApproachPaperCRUD.as_view(), name = 'Formulation Of Approach Paper CRUD'),

    # PSR Formulation Of Approach Paper Document
    path('psr/formulation_of_approach_paper_document',views.FormulationOfApproachPaperDocumentList.as_view(), name = 'Formulation Of Approach Paper Document List'),
    path('psr/formulation_of_approach_paper_document/crud',views.FormulationOfApproachPaperDocumentCRUD.as_view(), name = 'Formulation Of Approach Paper Document CRUD'),

    # PSR Formulation Of Approach Paper Send Email
    path('psr/formulation_of_approach_paper_send_email',views.FormulationOfApproachPaperSendMailList.as_view(), name = 'Formulation Of Approach Paper Send Email List'),
    path('psr/formulation_of_approach_paper_send_email/crud',views.FormulationOfApproachPaperSendMailCRUD.as_view(), name = 'Formulation Of Approach Paper Send Email CRUD'),




    # PSR Formulation Of Approach Responsibility 
    path('psr/formulation_of_approach_paper_responsibility',views.FormulationOfApproachPaperResponsibilityList.as_view(), name = 'formulation_of_approach_paper_responsibility'),
    path('psr/formulation_of_approach_paper_responsibility/crud',views.FormulationOfApproachPaperResponsibilityCRUD.as_view(), name = 'formulation_of_approach_paper_responsibility CRUD'),

    # PSR Presentation Of Approach Paper
    path('psr/presentation_of_approach_paper',views.PresentationOfApproachPaperList.as_view(), name = 'Presentation Of Approach Paper List'),
    path('psr/presentation_of_approach_paper/crud',views.PresentationOfApproachPaperCRUD.as_view(), name = 'Presentation Of Approach Paper CRUD'),

    # PSR Presentation Of Approach Paper Send Email             
    path('psr/presentation_of_approach_paper_send_email',views.PresentationOfApproachPaperSendMailList.as_view(), name = 'Presentation Send Email List'),
    path('psr/presentation_of_approach_paper_send_email/crud',views.PresentationOfApproachPaperSendMailCRUD.as_view(), name = 'Presentation Send Email CRUD'),

    # PSR Presentation Of Approach Paper Document
    path('psr/presentation_of_approach_paper_document',views.PresentationOfApproachPaperDocumentList.as_view(), name = 'Presentation Of Approach Paper Document List'),
    path('psr/presentation_of_approach_paper_document/crud',views.PresentationOfApproachPaperDocumentCRUD.as_view(), name = 'Presentation Of Approach Paper Document CRUD'),

    # PSR Inputs For Staff Requirement
    path('psr/inputs_for_staff_requirement',views.InputsForStaffRequirementList.as_view(), name = 'Inputs For Staff Requirement List'),
    path('psr/inputs_for_staff_requirement/crud',views.InputsForStaffRequirementCRUD.as_view(), name = 'Inputs For Staff Requirement CRUD'),
  
   # PSR Formulation Of Approach Paper Document
    path('psr/inputs_for_staff_requirement_document',views.InputsForStaffRequirementDocumentList.as_view(), name = 'Inputs For Staff Requirement Document List'),
    path('psr/inputs_for_staff_requirement_document/crud',views.InputsForStaffRequirementDocumentCRUD.as_view(), name = 'Inputs For Staff Requirement Document CRUD'),

    # PSR Formulation Of Approach Paper Send Email
    path('psr/inputs_for_staff_requirement_send_email',views.InputsForStaffRequirementSendMailList.as_view(), name = 'Inputs For Staff Requirement Send Email List'),
    path('psr/inputs_for_staff_requirement_send_email/crud',views.InputsForStaffRequirementSendMailCRUD.as_view(), name = 'Inputs For Staff Requirement Send Email CRUD'),

    # PSR Inputs For Staff Requirement Compartment
    path('psr/inputs_for_staff_requirement_compartment',views.InputsForStaffRequirementCompartmentList.as_view(), name = 'Inputs For Staff Requirement Compartment List'),

    # PSR Inputs For Staff Requirement Equipment
    path('psr/inputs_for_staff_requirement_equipment',views.InputsForStaffRequirementEquipmentList.as_view(), name = 'Inputs For Staff Requirement Equipment List'),

    # PSR Inputs For Staff Requirement System
    path('psr/inputs_for_staff_requirement_system',views.InputsForStaffRequirementSystemList.as_view(), name = 'Inputs For Staff Requirement System List'),

    # PSR Concept Design
    path('psr/concept_design',views.ConceptDesignList.as_view(), name = 'Concept Design List'),
    path('psr/concept_design/crud',views.ConceptDesignCRUD.as_view(), name = 'Concept Design CRUD'),
    
     # PSR Concept Design Document
    path('psr/concept_design_document',views.ConceptDesignDocumentList.as_view(), name = 'Concept Design Document List'),
    path('psr/concept_design_document/crud',views.ConceptDesignDocumentCRUD.as_view(), name = 'Concept Design Document CRUD'),

    # PSR Concept Design Send Email
    path('psr/concept_design_send_email',views.ConceptDesignSendMailList.as_view(), name = 'Concept Design Send Email List'),
    path('psr/concept_design_send_email/crud',views.ConceptDesignSendMailCRUD.as_view(), name = 'Concept Design Send Email CRUD'),

    # Incorporation Of Design Inputs
    path('psr/incorporation_of_design_inputs',views.IncorporationOfDesignInputsList.as_view(), name = 'Incorporation Of Design Inputs List'),
    path('psr/incorporation_of_design_inputs/crud',views.IncorporationOfDesignInputsCRUD.as_view(), name = 'Incorporation Of Design Inputs CRUD'),
 
     # PSR Incorporation Of Design Inputs Document
    path('psr/incorporation_of_design_inputs_document',views.IncorporationOfDesignInputsDocumentList.as_view(), name = 'Incorporation Of Design Inputs Document List'),
    path('psr/incorporation_of_design_inputs_document/crud',views.IncorporationOfDesignInputsDocumentCRUD.as_view(), name = 'Incorporation Of Design Inputs Document CRUD'),

    # PSR Incorporation Of Design Inputs Send Email
    path('psr/incorporation_of_design_inputs_send_email',views.IncorporationOfDesignInputsSendMailList.as_view(), name = 'Incorporation Of Design Inputs Send Email List'),
    path('psr/incorporation_of_design_inputs_send_email/crud',views.IncorporationOfDesignInputsSendMailCRUD.as_view(), name = 'Incorporation Of Design Inputs Send Email CRUD'),


    # RECEIPT OF RFI RESPONSES 
    path('psr/receipt_of_rfi_responses',views.ReceiptOfRFIResponsesList.as_view(), name = 'Receipt Of RFI Responses List'),
    path('psr/receipt_of_rfi_responses/crud',views.ReceiptOfRFIResponsesCRUD.as_view(), name = 'Receipt Of RFI Responses CRUD'),
   
    # PSR RECEIPT OF RFI RESPONSES Document
    path('psr/receipt_of_rfi_responses_document',views.ReceiptOfRFIResponsesDocumentList.as_view(), name = 'Receipt Of RFI Responses Document List'),
    path('psr/receipt_of_rfi_responses_document/crud',views.ReceiptOfRFIResponsesDocumentCRUD.as_view(), name = 'Receipt Of RFI Responses Document CRUD'),

    # PSR RECEIPT OF RFI RESPONSES Send Email
    path('psr/receipt_of_rfi_responses_send_email',views.ReceiptOfRFIResponsesSendMailList.as_view(), name = 'Receipt Of rfi Responses Send Email List'),
    path('psr/receipt_of_rfi_responses_send_email/crud',views.ReceiptOfRFIResponsesSendMailCRUD.as_view(), name = 'Receipt Of rfi Responses Send Email CRUD'),

    # PSR Responsibility
    path('psr/responsibility',views.ResponsibilityList.as_view(), name = 'Responsibility List'),
    path('psr/section_responsibility',views.ResponsibilitySectionList.as_view(), name = 'Responsibility Section List'),
    
    



    # GLS ###########################
    path('gls/document_sections', views.DocumentSectionsViews.as_view(), name = 'document_sections_views'),
    path('gls/document_sections/<int:pk>', views.DocumentSectionsViews.as_view(), name = 'view_document_sections'),
    path('gls/document_sections/details', views.DocumentSectionsDetailViews.as_view(), name = 'add_document_sections'),

    path('gls/document_sub_sections', views.DocumentSubSectionsViews.as_view(), name = 'document_sub_sections_views'),
    path('gls/document_sub_sections/<int:pk>', views.DocumentSubSectionsViews.as_view(), name = 'view_document_sub_sections'),
    path('gls/document_sub_sections/details', views.DocumentSubSectionsDetailViews.as_view(), name = 'add_document_sub_sections'),

    path('gls/document_sub_sections2', views.DocumentSubSections2Views.as_view(), name = 'document_sub_sections_views2'),
    path('gls/document_sub_sections2/<int:pk>', views.DocumentSubSections2Views.as_view(), name = 'view_document_sub_sections2'),
    path('gls/document_sub_sections2/details', views.DocumentSubSections2DetailViews.as_view(), name = 'add_document_sub_sections2'),

    path('gls/annexures', views.AnnexuresViews.as_view(), name = 'annexures'),
    path('gls/annexures/<int:pk>', views.AnnexuresViews.as_view(), name = 'view_annexures'),
    path('gls/annexures/details', views.AnnexuresDetailViews.as_view(), name = 'add_annexures'),

    # GLS Initiation Notes
    path('gls/initiation_notes_master',views.InitiationNotesGLSMasterList.as_view(), name = 'GLS Initiation Notes Master List'),
    path('gls/initiation_notes',views.InitiationNotesGLSList.as_view(), name = 'GLS Initiation Notes List'),
    path('gls/initiation_notes/<int:pk>',views.InitiationNotesGLSList.as_view(), name = 'GLS Initiation Notes List'),
    
    path('gls/initiation_notes/crud',views.InitiationNotesGLSCRUD.as_view(), name = 'GLS Initiation Notes CRUD'),
    path('gls/initiation_notes/master_crud',views.InitiationNotesGLSMasterCURD.as_view(), name = 'GLS Initiation Notes Master CRUD'),

    path('gls/initiation_notes/crud/delete', views.deleteInitiationNotesGLSMaster.as_view(), name="deleteInitiationNotesGLSMaster"),
    
    # GLS Initiation Notes Send Email
    path('gls/initiation_notes_send_email',views.GLSInitiationNotesSendMailList.as_view(), name = 'GLS Initiation Notes Send Email List'),
    path('gls/initiation_notes_send_email/crud',views.GLSInitiationNotesSendMailCRUD.as_view(), name = 'GLS Initiation Notes Send Email CRUD'),

     # GLS Initiation Notes  Document
    path('gls/initiation_notes_document',views.GLSInitiationNotesDocumentList.as_view(), name = 'GLS Initiation Notes Document List'),
    path('gls/initiation_notes_document/crud',views.GLSInitiationNotesDocumentCRUD.as_view(), name = 'GLS Initiation Notes Document CRUD'),


    # BLS Initiation Notes
    path('bls/initiation_notes_master',views.InitiationNotesBLSMasterList.as_view(), name = 'BLS Initiation Notes Master List'),

    path('bls/initiation_notes',views.InitiationNotesBLSList.as_view(), name = 'BLS Initiation Notes List'),
    path('bls/initiation_notes/crud',views.InitiationNotesBLSCRUD.as_view(), name = 'BLS Initiation Notes CRUD'),
    path('bls/initiation_notes/master_crud',views.InitiationNotesBLSMasterCURD.as_view(), name = 'BLS Initiation Notes Master CRUD'),

    path('bls/get_gls_initiation_notes',views.GetGLSInitiationNotesList.as_view(), name = 'Get GLS Initiation Notes Master List'),

    path('bls/initiation_notes/crud/delete', views.deleteInitiationNotesBLSMaster.as_view(), name="deleteInitiationNotesBLSMaster"),

     # BLS Initiation Notes Send Email
    path('bls/initiation_notes_send_email',views.BLSInitiationNotesSendMailList.as_view(), name = 'BLS Initiation Notes Send Email List'),
    path('bls/initiation_notes_send_email/crud',views.BLSInitiationNotesSendMailCRUD.as_view(), name = 'BLS Initiation Notes Send Email CRUD'),

     # BLS Initiation Notes  Document
    path('bls/initiation_notes_document',views.BLSInitiationNotesDocumentList.as_view(), name = 'BLS Initiation Notes Document List'),
    path('bls/initiation_notes_document/crud',views.BLSInitiationNotesDocumentCRUD.as_view(), name = 'BLS Initiation Notes Document CRUD'),



    # Common
    path('excel', views.ExportImportExcelGLS.as_view(), name="Excel"),
    path('bls/excel', views.ExportImportExcelBLS.as_view(), name="BLS Excel"),
    path('global_master', views.ListGlobalStatus.as_view(), name="ListGlobalStatus"),
    path('psr/initiation_notes/global_master', views.ListGlobalStatusInitiationNotes.as_view(), name="ListGlobalStatusInitiationNotes"),

    path('psr/formulation_of_approach_paper/global_master', views.ListGlobalStatusFormulationOfApproachPaper.as_view(), name="ListGlobalStatusFormulationOfApproachPaper"),
    path('psr/presentation_of_approach_paper/global_master', views.ListGlobalStatusPresentationOfApproachPaper.as_view(), name="ListGlobalStatusPresentationOfApproachPaper"),

    path('psr/inputs_for_staff_requirement_equipment/global_master', views.ListGlobalStatusInputsForStaffRequirement.as_view(), name="ListGlobalStatusInputsForStaffRequirement"),

    path('psr/concept_design/global_master', views.ListGlobalStatusConceptDesign.as_view(), name="ListGlobalStatusConceptDesign"),
    path('psr/incorporation_of_design_inputs/global_master', views.ListGlobalStatusIncorporationOfDesignInputs.as_view(), name="ListGlobalStatusIncorporationOfDesignInputs"),

    path('psr/receipt_of_rfi_responses/global_master', views.ListGlobalStatusReceiptOfRFIResponse.as_view(), name="ListGlobalStatusReceiptOfRFIResponse"),

    path('gls/initiation/global_master', views.ListGlobalStatusGLSInitiation.as_view(), name="ListGlobalStatusGLSInitiation"),

    path('psr/inputsr/ssr/crud', views.saveSSRForInputSR.as_view(), name="saveSSRForInputSR"),
    path('psr/inputsr/ssr/list', views.ListSSRForInputSR.as_view(), name="ListSSRForInputSR"),
    path('psr/inputsr/ssr/delete', views.deleteSSRForInputSR.as_view(), name="deleteSSRForInputSR"),

    path('psr/responsibility_list', views.ResponsibilityProject.as_view(), name="ResponsibilityProject"),

    path('ssr_list', views.ListSSRForProject.as_view(), name="ListSSRForProject"),

    path('save_responsibility', views.saveResponsibility.as_view(), name="saveResponsibility"),
    path('get_responsibility', views.getResponsibility.as_view(), name="getResponsibility"),
    path('get_responsibility_other', views.getResponsibilityOther.as_view(), name="getResponsibilityOther"),
    path('get_responsibility_section', views.getResponsibilitySection.as_view(), name="getResponsibilitySection"),

    path('save_inputSR', views.saveInputSR.as_view(), name="saveInputSR"),
    path('save_conceptDesign', views.saveConceptDesign.as_view(), name="saveConceptDesign"),
    path('save_incorporation', views.saveInCorporation.as_view(), name="saveInCorporation"),
    path('saveRFI', views.saveRFI.as_view(), name="saveRFI"),
    path('saveRFISections', views.saveRFISections.as_view(), name="saveRFISections"),
    path('get_complete_psr', views.getCompletePSR.as_view(), name="getCompletePSR"),
    path('get_general_ref_for_inputsr', views.getGeneralRefForInputSR.as_view(), name="getGeneralRefForInputSR"),

    path('get_section_general', views.getSectionGeneral.as_view(), name="getGeneralRefForInputSR"),
    # path('psr/input_staff_responsibility', views.InputStaffResponsibilityList.as_view(), name="InputStaffResponsibilityList")  


    # Dashboard

    #path('dashboard/project_list', views.getProjectList.as_view(), name="getProjectList"),
    
    path('dashboard/project_list', views.getAllProjectList.as_view(), name="getAllProjectList"),
    path('dashboard/project_detail', views.getProjectDetail.as_view(), name="getProjectDetail"),

    path('dashboard/module', views.getDashBoardModule.as_view(), name="getDashBoardModule"),
    path('dashboard/module_psr', views.getDashBoardModulePSR.as_view(), name="getDashBoardModulePSR"),

    # Global Transaction
    path('global_transaction',views.GlobalTransactionViews.as_view(), name = 'Global Transaction'), 
    path('global_transaction_list',views.GlobalTransactionEditViews.as_view(), name = 'Global Transaction Edit'),

    # Add
    path('global_transaction_details', views.GlobalTransactionDetailsViews.as_view(), name="Global Transaction Details"),

    # Edit
    path('global_transaction_details_edit', views.GlobalTransactionDetailsViewsEdit.as_view(), name="Global Transaction Details Edit"),

    # Delete
    path('global_transaction_details_delete', views.GlobalTransactionDetailsViewsDelete.as_view(), name="Global Transaction Details Delete"),


    path('global_transaction/report/<id>',views.global_transaction, name = 'Global'),
    path('global_transaction_gls/report/<id>',views.global_transaction_gls, name = 'Global'),
    path('global_transaction_bls/report/<id>',views.global_transaction_bls, name = 'Global'),
    path('global_transaction_submodule/report/<id>/<form_id>',views.global_transaction_submodule, name = 'Global'),
    path('global_transactionpdf/report/<id>',views.global_transactionpdf, name = 'Global'),
    path('global_transaction_glspdf/report/<id>',views.global_transaction_glspdf, name = 'Global'),
    path('global_transaction_blspdf/report/<id>',views.global_transaction_blspdf, name = 'Global'),

    path('global_transaction_edit',views.GlobalTransactionEdit.as_view(), name = 'Global Transaction Edit'),
    
    # Get List
    path('global_transaction_edit_1',views.GlobalTransactionEdit_1.as_view(), name = 'Global Transaction Edit'),


    path('global_transaction_download',views.GlobalTransactionDownload.as_view(), name = 'Global Transaction download'),

    path('global_transaction_approve_status',views.GlobalTransactionApproveStatus.as_view(), name = 'Global Transaction Approve Status'),

    path('approve_list', views.ListGlobalStatus1.as_view(), name="ListGlobalStatus1"),



    path('gt_global_master', views.GTListGlobalStatus.as_view(), name="GTListGlobalStatus"),
    ###########

    path('sss_mapping/details', views.SSSMappingDetailViews.as_view(), name="SSSMappingDetailViews"),
    path('sss_mapping', views.SSSMappingViews.as_view(), name="SSSMappingViews"),

    ########## Global Transation - Internal Mapping ############
    path('gt_internal_mapping', views.GTInternalMappingViews.as_view(), name="GT Internal Mapping Views"),


    #### Forms Mapping ####

    path('forms', views.FormsViews.as_view(), name="Forms Views"),
    path('forms-without-mapping', views.FormsWOTMappingViews.as_view(), name="Forms Views"),
    path('forms_mapping', views.FormsMappingViews.as_view(), name="Forms Mapping Views"),
    path('forms_mapping_details', views.FormsMappingDetailsViews.as_view(), name="Forms Mapping Details"),
    #path('forms_mapping_details', views.TestFormsMappingDetailsViews.as_view(), name="Forms Mapping Details"),
    path('forms_map', views.MappingListViews.as_view(), name="Mapping Views"),
    path('forms-template', views.getFormMapping.as_view(), name="getFormMapping"),
    path('get-all-psr', views.getFormMappingAllPSR.as_view(), name="getFormMappingAllPSR"),

    ### Generate Template ###
    path('generate_template', views.GenerateTemplateViews.as_view(), name="Generate Template"),

    path('global/transactions/save', views.saveGlobalTransactionDetails.as_view(), name="Global Transaction Details"),
    # path('global/transactions/log', views.saveGlobalTransactionlog.as_view(), name="Global Transaction Details Log"),
    path('global/transactions/delete', views.deleteGlobalTransactionDetails.as_view(), name="Global Transaction Delete"),
    path('global/transactions',views.getGlobalTransactions.as_view(), name = 'Global Transactions'),
    path('form-name',views.getFormName.as_view(), name = 'getFormName'),
    path('sample-test',views.sampleTest.as_view(), name = 'sampleTest'),
    path('get-sss',views.getSSS.as_view(), name = 'getSSS'),

    path('add-version', views.addVersion.as_view(), name="addVersion"),
    path('version', views.Version.as_view(), name="Version"),
    path('get-version', views.getVersion.as_view(), name="getVersion"),
    path('version_transaction/report/<id>',views.version_transaction, name = 'Version Transaction'),

    path('save_transaction_responsibility', views.saveTransactionResponsibility.as_view(), name="saveTransactionResponsibility"),

    path('delete_transaction_responsibility', views.deleteTransactionResponsibility.as_view(), name="deleteTransactionResponsibility"),

    path('global_transaction_responsibility', views.GlobalTransactionResponsibility.as_view(), name="Version"),

    path('global/transactions_comments/save', views.saveGlobalTransactionCommentsDetails.as_view(), name="Global Transaction Comments Details"),
    
    path('global/transactions_comments/delete', views.deleteGlobalTransactionCommentsDetails.as_view(), name="Global Transaction Comments Delete"),

    path('approved_history',views.ApprovalHistory.as_view()),

    path('global/approval',views.GlobalApproval.as_view(), name = 'Global Approval'),
    
    path('modulewise-timeline',views.getModulewiseTimeline.as_view(), name = 'getModulewiseTimeline'),

   
    path('projectlog',views.ProjectLog.as_view(), name = 'Project log'),
    

    path('global/system_equipment_compartment_temp/save', views.saveSystemEquipmentCompartmentTemp.as_view(), name="System Equipment Compartment Temp"),

    # PDF Edit #
    path('global_transaction_get_pdf/report/<id>', views.global_transaction_get_pdf, name="Global Transaction Get PDF"),

    path('global_transaction_get_gls_pdf/report/<id>', views.global_transaction_get_gls_pdf, name="Global Transaction Get GLS PDF"),

    path('global_transaction_get_bls_pdf/report/<id>', views.global_transaction_get_bls_pdf, name="Global Transaction Get BLS PDF"),

    path('global_transaction_edit_pdf/report',views.globalTransactionEditPDF.as_view(), name = 'Global Transaction Edit PDF'),

    path('global_transaction_gen_edit_pdf/report',views.global_transaction_gen_edit_pdf, name = 'Global Transaction Gen Edit PDF'),


    path('all_forms', views.AllFormsView.as_view(), name="All Forms Views"),
    path('get_form_mapping', views.GetFormsView.as_view(), name="Get Forms Views"),
    path('convert_pdf_word/<id>', views.convert_pdf_word, name="All Forms Views"),

    path('get_form_level_hierarchy', views.GetFormLevelHierarchy.as_view(), name="Get Forms Level Hierarchy"),
    path('forms_level_hierarchy_details', views.FormLevelHierarchyViews.as_view(), name="Form Level Hierarchy Views"),

    path('get_project_level_hierarchy', views.GetProjectLevelHierarchy.as_view(), name="Get Project Level Hierarchy"),
    path('project_level_hierarchy_details', views.ProjectLevelHierarchyViews.as_view(), name="Project Level Hierarchy Views"),

    path('save_hierarchy_level', views.SaveHierarchyLevel.as_view(), name="Save Hierarchy Level"),
    path('ship_details', views.ShipDetailsViews.as_view(), name="Save Ship Details"),
    path('get_ship_details', views.GetShipDetails.as_view(), name="Get Ship Details"),

    path('test_excel_export', views.TestExcelExport.as_view(), name="test_excel_export"),


    # Dockyard #    
    path('dart',views.DartList.as_view(), name = 'Dart List'),
    path('dart/crud',views.DartCRUD.as_view(), name = 'Dart CRUD'),
    path('dart/excel', views.ImportExcelDart.as_view(), name="Dart Excel"),

    path('ra',views.RAList.as_view(), name = 'RA List'),
    path('ra/crud',views.RACRUD.as_view(), name = 'RA CRUD'),
    path('ra/excel', views.ImportExcelRA.as_view(), name="RA Excel"),

]
