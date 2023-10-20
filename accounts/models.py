from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from access.models import Process
#from master.models import Designation
#from django.db import models
# from django.apps import apps
# Designation = apps.get_model('master', 'Designation')
    
# from django.db.models import get_model
# Designation = get_model('master', 'Designation')


# from django.apps import apps

# Designation = get_model('master', 'Designation')
#from django.db.models.master import get_model
#Designation = get_model('master', 'Designation')

class UserManager(BaseUserManager):
    def create_user(self,loginname,first_name,email,last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not loginname:
            raise ValueError('Users must have an login name')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.loginname=loginname
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, loginname, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            loginname,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, loginname,first_name,email,last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            loginname,
            first_name,
            email,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    loginname = models.CharField(
        verbose_name='login name',
        max_length=255,
        unique=True,
        default='',
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=255,
        unique=False,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=255,
        unique=False,
        blank=True,
    )
    process =models.ForeignKey(Process,on_delete=models.CASCADE,null=True,blank=True,default=1)
    #desig = models.ForeignKey('master.Unit', on_delete = models.CASCADE, null = True)
    icard_number = models.CharField(max_length=100, null=True, blank=True)
    design = models.ForeignKey('master.Designation', on_delete = models.CASCADE, null = True)
    category_type = models.ForeignKey('master.CategoryType', on_delete = models.CASCADE, null = True)
    pay_scale = models.ForeignKey('master.PayScale', on_delete = models.CASCADE, null = True)
    center = models.ForeignKey('master.Center', on_delete = models.CASCADE, null = True)
    shop_floor = models.ForeignKey('master.Shopfloor', on_delete = models.CASCADE, null = True)
    pay_grade = models.ForeignKey('master.PayGrade', on_delete = models.CASCADE, null = True)
    current_basic_salary = models.DecimalField(max_digits = 6, decimal_places = 2, null=True, blank=True)    
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    fpdata = models.TextField(null= True)
    verification_code = models.CharField(max_length= 6, null= True)
    status = models.SmallIntegerField(choices=((1, 'Active'), (2, 'Inactive'), (3, 'Delete')), default= 1)

    objects = UserManager()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'loginname'
    REQUIRED_FIELDS = ['first_name','last_name','email'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin