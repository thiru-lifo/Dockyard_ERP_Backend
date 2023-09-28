from django.db import models

# Create your models here.
class IPL(models.Model):
    team = models.CharField(max_length=5)
    captain = models.CharField(max_length= 25)
    city = models.CharField(max_length=25)

    def __str__(self):
        return self.team

    class Meta:
        db_table = 'export.ipl'
        verbose_name = "IPL"
        verbose_name_plural = "IPL"
