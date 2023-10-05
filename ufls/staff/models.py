import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    departmentHead = models.ForeignKey(
        User,
        models.SET_NULL,
        "deptHead",
        "Department Staff Director",
        blank=True,
        null=True,
    )
    departmentSecond = models.ForeignKey(
        User,
        models.SET_NULL,
        "deptSecond",
        "Department Staff Assistant Director",
        blank=True,
        null=True,
    )
    departmentBoard = models.ForeignKey(
        User,
        models.SET_NULL,
        "deptBoardMember",
        "Department Assigned Board Member",
        blank=True,
        null=True,
    )
    parentDepartment = models.ForeignKey(
        "staff.Department",
        models.SET_NULL,
        "parentDepartmentRef",
        "Parent Department",
        blank=True,
        null=True,
    )

    def getStaff(self):
        return StaffAssignment.objects.filter(department=self, rank="Staff")

    def getOpenPositions(self):
        return OpenPosition.objects.filter(department=self, hidden=False)

    def getOpenApplications(self):
        return StaffApplication.objects.filter(openPosition__department=self, closeApp=False)

    def __str__(self):
        return self.name


class OpenPosition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    department = models.ForeignKey("staff.Department", on_delete=models.CASCADE)
    need = models.IntegerField()
    hidden = models.BooleanField(
        help_text="Toggle this if you don't want this to show in the Open Positions Catalogue"
    )

    def __str__(self):
        return self.name

class LicenseKey(models.Model):
    PROGRAMS = (
        ("ios-pocketsec", "PocketSec (iOS)"),
        ("ios-regapp", "RegApp (iOS)")
    )
    key = models.CharField(max_length=100)
    program = models.CharField(choices=PROGRAMS, max_length=35)
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class StaffAssignment(models.Model):
    RANKS = (
        ("Staff", "Staff Member"),
        ("Department Assistant Director", "Department Assistant Director"),
        ("Department Director", "Department Director"),
        ("Board Member", "Board Member"),
        ("Volunteer", "Volunteer")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey("staff.Department", on_delete=models.CASCADE)
    rank = models.CharField(max_length=50, choices=RANKS)
    title = models.CharField(max_length=50, blank=True, null=True)
    primary_assignment = models.BooleanField(default=False)
    grant_access_to_management_panel = models.BooleanField(default=False, help_text="Grants access to the management panel for this department if the staff is a Member and not a management position.")

    PERMS = {
        "staff-portal": {"view": False, "edit": False, "manage": False},
        "volunteer-portal": {"view": False, "edit": False, "manage": False},
        "events-manage": {"view": False, "edit": False, "manage": False},
        "app-manage": {"view": False, "edit": False, "manage": False},
        "registration-manage": {"view": False, "edit": False, "manage": False},
        "marketplace-manage": {"view": False, "edit": False, "manage": False},
        "staff-manage": {"view": False, "edit": False, "manage": False},
        "volunteer-manage": {"view": False, "edit": False, "manage": False}
    }

    permissions_matrix = models.JSONField(blank=True, null=True, default=PERMS)

    def showDisplayName(self):
        if self.displayName == "" or self.displayName == None:
            return self.user.first_name
        return self.displayName

    def __str__(self):
        return "%s / %s" % (self.user.username, self.department.name)

    def showDisplayTitle(self):
        if self.title == "" or self.title == None:
            return self.get_rank_display()
        return self.title

class StaffApplication(models.Model):
    firstName = models.CharField("Legal First Name", max_length=100)
    lastName = models.CharField("Legal Last Name", max_length=100)
    fanName = models.CharField("Furry or Fan Name", max_length=100)
    dateOfBirth = models.DateField("Date of Birth")
    felonyVerify = models.BooleanField(
        "Certify no felonies",
        help_text="I certify that I have not been convicted of a felony",
    )
    eighteenVerify = models.BooleanField(
        "18+ Verification",
        help_text="I certify that I will be aged 18 or older at the time of the convention.",
    )
    covidCert = models.BooleanField(
        "Certify COVID-19 Vaccination",
        help_text="I certify that I have recieved my full series of vaccinations against COVID-19 and am considered Fully Vaccinated. (This is non-negotiable and must be certified)",
        default=False
    )
    openPosition = models.ForeignKey(
        "staff.OpenPosition", blank=True, null=True, on_delete=models.SET_NULL
    )
    address1 = models.CharField("Address 1", max_length=100)
    address2 = models.CharField("Address 2", max_length=100, blank=True, null=True)
    city = models.CharField("City", max_length=100)
    state = models.CharField("State", max_length=100)
    zipCode = models.CharField("ZIP Code", max_length=100)
    emergencyContact = models.CharField("Emergency Contact Name", max_length=100)
    emergencyContactRelation = models.CharField(
        "Emergency Contact Relation", max_length=100
    )
    emergencyContactNumber = models.CharField(
        "Emergency Contact Phone Number", max_length=100
    )
    email = models.EmailField("E-Mail Address", max_length=100)
    telegramHandle = models.CharField(
        "Telegram Handle", max_length=100, blank=True, null=True
    )
    fitness = models.TextField("Why would you be a good fit for staff?")
    about = models.TextField(
        "Tell us about your skills you would bring to Furrydelphia"
    )
    experience = models.TextField(
        "Have you worked for any other conventions? Tell us about it.",
        blank=True,
        null=True,
    )
    other = models.TextField(
        "Anything else you would like us to know?", blank=True, null=True
    )
    closeApp = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fanName}'s application for {self.openPosition}"


class TaskTemplate(models.Model):
    action = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    dueDate = models.DateTimeField()
    fromDepartment = models.ForeignKey("staff.Department", on_delete=models.CASCADE)
    departmentOnly = models.BooleanField(default=False)


class StaffTask(models.Model):
    template = models.ForeignKey("staff.TaskTemplate", on_delete=models.CASCADE)
    user = models.ForeignKey("staff.StaffAssignment", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField(blank=True, null=True)


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    fromDepartment = models.ForeignKey("staff.Department", on_delete=models.CASCADE)
    departmentOnly = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    _from = models.CharField(
        max_length=100, blank=True, null=True, default="Department Lead"
    )

class Policy(models.Model):
    staff_general = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('staff.Department', on_delete=models.PROTECT)
    last_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    weight = models.IntegerField(default=0)