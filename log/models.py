from django.db import models
from accounts.models import User


class UserLogin(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    logon_type = models.CharField(max_length=150)
    log_datetime = models.DateTimeField(auto_now_add=True)
    log_ip = models.GenericIPAddressField()
    log_browser = models.CharField(max_length=100,null= True, blank= True)
    log_version = models.CharField(max_length=100,  blank=True, null=True)
    log_os = models.CharField(max_length=100, null= True, blank= True)
    log_platform = models.CharField(max_length=100, null= True, blank= True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table ='log.user_login' 
        verbose_name = "User Login"
        verbose_name_plural = "User Login"




