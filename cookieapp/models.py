from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from customer.models import Tenant
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_admin_user(self, email, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user  # Add return statement here to return the superuser
    
    def create_super_user(self, email, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser =True
        user.save(using=self._db)
        return user  # Add return statement here to return the superuser



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=False, blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenent  = models.OneToOneField(Tenant,null=True,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200,default='ABC')
    company_logo = models.ImageField(upload_to='logo',null=True)
    objects = AccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email  # Fix: Return the email field instead of username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
