"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import Group, Permission


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    ADMIN = 'admin'
    EXAMINEE = 'examinee'
    ROLE_CHOICES = [
        (EXAMINEE, 'Examinee'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Modified_Date = models.DateTimeField(auto_now=True)
    # role = models.Choices(
    #     max_length=20,
    #     choices=ROLE_CHOICES,
    #     default="Exa"
    # )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.ForeignKey('Choice', on_delete=models.CASCADE)
    choices = models.ManyToManyField('Choice', related_name='questions')

    def __str__(self):
        return self.question


class Choice(models.Model):
    choice = models.CharField(max_length=255)

    def __str__(self):
        return self.choice


class Examinee_Answer(models.Model):
    examinee_answer = models.CharField(max_length=255)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    issubmitted = models.BooleanField(default=False)
    iscorrect = models.BooleanField(default=False)
    isbookmarked = models.BooleanField(default=False)
    # examinee = models.ForeignKey(Examinee, on_delete=models.CASCADE)

    def __str__(self):
        return self.examinee_answer