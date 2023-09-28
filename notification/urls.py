from django.urls import path
from . import views


urlpatterns = [
    path('notify',views.NotificationViews.as_view(), name = 'notify'),
    path('email-verify', views.VerifyEmail.as_view(), name = 'email-verify'),
    path('smtp', views.SmtpconfigureViews.as_view(), name = 'smtp'),
    path('get-notifications',views.getNotifications.as_view(), name = 'notify'),
    path('save-notification-log',views.saveNotificationLog.as_view(), name = 'notify'),
   
]