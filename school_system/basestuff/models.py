from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ExtendBaseUser(models.Model):
    middle_name = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField()
    user_type = models.CharField(max_length=10, choices=(( 'teacher','teacher'), ('student', 'student')), default=1)
    image = models.ImageField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Classroom(models.Model):
    title = models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Subject(models.Model):
    subject_name = models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Mark(models.Model):
    mark = models.PositiveIntegerField()
    date = models.DateTimeField()
    description = models.TextField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class BehavioralAssessment(models.Model):
    title = models.CharField(max_length=20)
    date = models.DateTimeField()
    description = models.TextField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
