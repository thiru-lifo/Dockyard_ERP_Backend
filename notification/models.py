from django.db import models
import os
from twilio.rest import Client
from access.models import AccessUserRoles,Process
from accounts.models import User
from master import models as masterModels
from transaction import models as transactionModels

class NotificationUser(models.Model):

    # module =models.ForeignKey(masterModels.Module,on_delete=models.CASCADE,null=True,blank=True)
    # sub_module =models.ForeignKey(masterModels.SubModule,on_delete=models.CASCADE,null=True,blank=True)
    hierarchy_type = models.SmallIntegerField(choices=((1,'initiator'),(2,'Recommender'),(3,'Approver')), null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to_user')
    form = models.ForeignKey(transactionModels.Forms,on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(masterModels.Project,on_delete=models.CASCADE,null=True,blank=True)
    user_role = models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,null=True,blank=True)
    transaction = models.ForeignKey(transactionModels.GlobalTransaction,on_delete=models.CASCADE,null=True,blank=True)
    process = models.ForeignKey(Process,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notification.user_notifications'
        verbose_name = "User Notification"
        verbose_name_plural = "User Notifications"

class NotificationUserLog(models.Model):

    notification =models.ForeignKey(NotificationUser,on_delete=models.CASCADE)
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    user_role =models.ForeignKey(AccessUserRoles,on_delete=models.CASCADE,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notification.user_notifications_log'
        verbose_name = "User Notification Log"
        verbose_name_plural = "User Notifications Log"

class Notification(models.Model):

    title = models.CharField(max_length= 100)
    type = models.SmallIntegerField(choices=((1,'SMS'),(2,'Email'), (3,'Internet'),))
    subject = models.CharField(max_length= 50, null= True, blank= True)
    message = models.CharField(max_length= 200)
    to =models.TextField()
    cc = models.EmailField(null= True, blank= True)
    bcc = models.EmailField(null= True, blank= True)
    attachment = models.FileField(null= True, blank= True, upload_to='media/')
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notify'
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class Smtpconfigure(models.Model):
    email_use_tls = models.BooleanField((u'EMAIL_USE_TLS'),default=True)
    email_host = models.CharField((u'EMAIL_HOST'),max_length=1024)
    email_host_user = models.CharField((u'EMAIL_HOST_USER'),max_length=255)
    email_host_password = models.CharField((u'EMAIL_HOST_PASSWORD'),max_length=255)
    email_port = models.PositiveSmallIntegerField((u'EMAIL_PORT'),default=587)

    def __str__(self):
        return self.email_host_user

    class Meta:
        db_table = 'smptconfigure'
