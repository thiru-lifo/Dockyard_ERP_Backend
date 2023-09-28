from django.urls import path
from . import views

urlpatterns = [

path('modules', views.ModuleViews.as_view(), name = 'viewmodules'),
path('modules/<int:pk>', views.ModuleViews.as_view(), name = 'viewmodule'),
path('modules/details', views.ModuleDetailViews.as_view(), name = 'addmodules'),

path('modulecomponents', views.ModulesComponentsViews.as_view(),name='viewmodules'),
path('modulecomponents/<int:pk>', views.ModulesComponentsViews.as_view(),name = 'viewmodule'),
path('modulecomponents/details', views.ModulesComponentsDetail.as_view(),name = 'addmodule'),

path('module_components_attribute', views.ModulesComponentsAttributeViews.as_view(),name='view_component_attribute'),
path('module_components_attribute/<int:pk>', views.ModulesComponentsAttributeViews.as_view(),name = 'view_component_attribute'),
path('module_components_attribute/details', views.ModulesComponentsAttributeDetail.as_view(),name = 'add_component_attribute'),

path('access_user_roles', views.AccessUserRolesView.as_view(), name = 'view_access_user_roles'),
path('access_user_roles/<int:pk>', views.AccessUserRolesView.as_view(), name = 'view_access_user_roles'),
path('access_user_roles/details', views.AccessUserRolesDetailsView.as_view(), name = 'add_access_user_roles'),

path('access_modules', views.AccessModulesView.as_view(), name = 'view_acces_modules'),
path('access_modules/<int:pk>', views.AccessModulesView.as_view(), name = 'view_access_modules'),
path('access_modules/details', views.AccessModulesDetailsView.as_view(), name = 'add_access_modules'),

path('privileges', views.PrivilegesView.as_view(), name = 'view_privileges'),
path('privileges/<int:pk>', views.PrivilegesView.as_view(), name = 'view_privileges'),
path('privileges/details', views.PrivilegesDetailsView.as_view(), name = 'add_privileges'),

path('permissions', views.PermissionsView.as_view(), name = 'view_permissions'),
path('permissions/<int:pk>', views.PermissionsView.as_view(), name = 'view_permissions'),
path('permissions/details', views.PermissionsDetailsView.as_view(), name = 'add_permissions'),


path('allmodules', views.AllModuleViews.as_view(), name = 'viewmodules'),
path('process', views.ProcessViews.as_view(), name = 'viewmodules'),


# User Role
path('user_role', views.UserRoleView.as_view(), name = 'view_user_role'),
path('user_role/<int:pk>', views.UserRoleView.as_view(), name = 'view_user_role'),
path('user_role/details', views.UserRoleDetailsView.as_view(), name = 'add_user_role'),

# path('user_role_designation', views.UserRoleDesignation.as_view(), name = 'view_user_role_designation'),
# path('user_role_designation/<int:pk>', views.UserRoleDesignation.as_view(), name = 'view_user_role_designation'),
# path('user_role_designation/details', views.UserRoleDesignation.as_view(), name = 'add_user_role_designation'),


]