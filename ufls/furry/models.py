from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emailMe = models.BooleanField(default=False)
    key = models.UUIDField(unique=True,primary_key=True,default=uuid.uuid4)
    preferredName = models.CharField(max_length=100, blank=True, null=True)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    restricted = models.BooleanField(default=False)
    staffManager = models.ForeignKey('furry.Profile', related_name="direct_staff_report", blank=True, null=True, on_delete=models.SET_NULL)
    staffBoardMember = models.ForeignKey('furry.Profile', related_name="board_member_responsible", blank=True, null=True, on_delete=models.SET_NULL)
    isStaff = models.BooleanField(default=False)
    isDepartmentHead = models.BooleanField(default=False)
    department = models.ForeignKey('furry.Department', blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.user.username

class EmailValidation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4)
    used = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    usedFor = models.CharField(max_length=100, default='Generic')

class RoomMonitor(models.Model):
    name = models.SlugField(unique=True, max_length=50, primary_key=True)
    display_name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)

class RoomMonitorHistory(models.Model):
    room = models.ForeignKey('furry.RoomMonitor', on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()

class RegistrantAssociationKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    account = models.ForeignKey('furry.Profile', on_delete=models.CASCADE)
    registrant = models.ForeignKey('registration.RegistrantData', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)