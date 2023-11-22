"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Modified_Date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Question(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.answer


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE
        )
    choice = models.CharField(max_length=200)

    def __str__(self):
        return self.choice

    @classmethod
    def save_choices(cls, question, choices_list):
        """
        Save a list of choices to the Choice model for a question.
        """
        choices_str = ', '.join(choices_list)
        cls.objects.create(question=question, choice=choices_str)

    @classmethod
    def get_choices(cls, question):
        """
        Get a list of choices for a question.
        """
        choices_str = cls.objects.get(question=question).choice
        return choices_str.split(', ')
