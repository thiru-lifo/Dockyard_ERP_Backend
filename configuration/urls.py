from django.urls import path
from . import views

urlpatterns = [
    path('configuration_table',views.ConfigurationTableViews.as_view(), name = 'viewconfiguration'),
    path('configuration_table/<int:pk>',views.ConfigurationTableViews.as_view(), name = 'viewconfigure'),
    path('configuration_table/details',views.ConfigurationTableDetailViews.as_view(), name = 'addconfiguration'),
 
    
    path('template_table',views.TemplatetableViews.as_view(), name = 'viewtemplate table'),
   	path('template_table/<int:pk>',views.TemplatetableViews.as_view(), name = 'viewtemplate table'),
    path('template_table/details',views.TemplatetableDetailViews.as_view(), name = 'addtemplate_table'), 

    path('template_country',views.TemplateCountryViews.as_view(), name = 'viewtemplate country'),
   	path('template_country/<int:pk>',views.TemplateCountryViews.as_view(), name = 'viewtemplate country'),
    path('template_country/details',views.TemplateCountryDetailViews.as_view(), name = 'addtemplate_country'),

    path('approvals', views.approvalList.as_view(), name='Approval List'),
    path('approvals/crud', views.approvalCRUD.as_view(), name='Approval CRUD'),

]
