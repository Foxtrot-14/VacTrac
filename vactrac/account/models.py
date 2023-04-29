from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
USER_TYPE = (
    (1,"Parent"),
    (2,"Doctor"),
    (3,"Crew"),
)
class UserManager(BaseUserManager):
    def create_user(self, phone, name, type, otp, is_verified=False, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, team_name and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone=phone,
            name=name,
            type=type,
            otp=otp,
            is_verified=is_verified,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, type, name, otp=0000, password=None):
        """
        Creates and saves a superuser with the given email, name,teamname and password.
        """
        user = self.create_user(
            phone,
            password=password,
            name=name,
            type=type,
            otp=otp,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone = models.CharField(
        verbose_name='Phone',
        max_length=15,
        unique=True,
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    type = models.IntegerField(choices=USER_TYPE)
    otp = models.IntegerField(default=1234)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name','type']

    def __str__(self):
        return self.name
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin