from django.urls import path
from . import views

urlpatterns = [
    path('userlogin',views.UserLoginViews.as_view(), name = 'login'),
    path('userlogin/<int:pk>', views.UserLoginViews.as_view(), name = 'view_login'),
    path('userlogin/details', views.UserLoginDetailViews.as_view(), name = 'add_login')

]    