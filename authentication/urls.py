from django.urls import path
from . import views

urlpatterns = [
    path('token', views.MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('logout', views.LogoutView.as_view(), name = 'logout_api'),
    path('authentications', views.authenticationView.as_view(), name = 'logout_api'),
    path('resend-code', views.ResendCodeView.as_view(), name = 'logout_api'),
    #path('token/refresh', views.MyTokenRefreshView.as_view(), name= 'refreshtoken'),
    path('verifyemailverificationcode', views.CorrectVerificationCode.as_view(), name='verifyemailverificationcode'),
    path('change-password', views.ChangePasswordAPI.as_view()),
    path('users', views.userList.as_view(), name='User List'),
    path('users_hierarchy', views.userListHierarchy.as_view(), name='User List Hierarchy'),
    path('users/crud', views.usersCRUD.as_view(), name='User CRUD'),
    path('users/import_excel', views.userImport.as_view(), name='User Import'),

    path('user/get_user', views.getUser.as_view(), name='Get User'),
]