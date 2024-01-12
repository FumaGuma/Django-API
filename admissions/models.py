from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from admissions.utils import UserManager
from django.core.exceptions import ValidationError


class Major(models.Model):
    name = models.CharField(max_length=100)
    quota = models.IntegerField()
    occupancy = models.IntegerField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=2000)
    ects_points = models.IntegerField()
    major = models.ForeignKey(Major, on_delete=models.CASCADE)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )
    first_name = models.CharField(
        max_length=30,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
    )
    enrolled_major = models.ForeignKey(
        Major, on_delete=models.CASCADE, blank=True, null=True
    )
    objects = UserManager()
    USERNAME_FIELD = "email"


class Application(models.Model):
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=50)
    previous_school = models.CharField(max_length=50)
    previous_school_diploma = models.FileField()
    gpa = models.FloatField()
    final_exams_grade = models.FloatField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.major.name


class Approval(models.Model):
    explanation = models.CharField(max_length=2000)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not User.objects.get(pk=self.admin.id).is_admin:
            raise ValidationError("Specified user is not an admin!")
        if User.objects.get(pk=self.student.id).is_admin:
            raise ValidationError("Specified user is not a student!")
