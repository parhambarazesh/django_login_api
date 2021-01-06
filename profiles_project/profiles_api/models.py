from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles

    Args:
        BaseUserManager ([type]): [description]

    Returns:
        [type]: [description]
    """
    def create_user(self,email,name,password=None):
        """Create a new user profile

        Args:
            email ([type]): [description]
            name ([type]): [description]
            password ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        if not email:
            raise ValueError('User must have an email address')

        email=self.normalize_email(email)
        user=self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,name,password):
        """Create and save a new superuser with given details

        Args:
            email ([type]): [description]
            name ([type]): [description]
            password ([type]): [description]

        Returns:
            [type]: [description]
        """
        user=self.create_user(email,name,password)

        #is_superuser is automatically created by PermissionsMixin imported! we have not defined it in the model manually.
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system

    Args:
        AbstractBaseUser ([type]): [description]
        PermissionsMixin ([type]): [description]
    """

    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']
    
    def get_full_name(self):
        """Retrieve full name of the user
        """
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of the user
        """
        return self.name
    
    def __str__(self):
        """Return string representation of our user
        """
        return self.email