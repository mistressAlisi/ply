from django.db import models
from slugify import slugify

# Create your models here.


class StaffOnboardRecord(models.Model):
    RANKS = (
        ("Staff", "Staff Member"),
        ("Department Assistant Director", "Department Assistant Director"),
        ("Department Director", "Department Director"),
    )
    DISPLAYS = (
        ("0", "<First Name> <Last Name>"),
        ("1", "<Fan Name> <Last Name>"),
        ("2", "<Fan Name>"),
    )
    USERNAMEDISPLAYS = (
        ("0", "<Fan Name>@staff.furrydelphia.org"),
        ("1", "<First Initial><Last Name>@staff.furrydelphia.org"),
        ("2", "<Fan Name First Initial><Last Name>@staff.furrydelphia.org"),
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    fanName = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    email = models.EmailField(
        max_length=100,
        help_text="This will be the e-mail address used to send a welcome letter to the staff member.",
    )
    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="In this format: +1 555 555 5555",
    )
    telegramHandle = models.CharField(max_length=100, blank=True, null=True)
    openPosition = models.ForeignKey(
        "staff.OpenPosition", blank=True, null=True, on_delete=models.SET_NULL
    )
    department = models.ForeignKey(
        "staff.Department", on_delete=models.SET_NULL, blank=True, null=True
    )
    rank = models.CharField(max_length=100, default="Staff", choices=RANKS)
    title = models.CharField("Custom Title", max_length=100, blank=True, null=True)
    displayNameAs = models.CharField(choices=DISPLAYS, max_length=1, default="0")
    usernameAs = models.CharField(choices=USERNAMEDISPLAYS, max_length=1, default="0")
    created = models.BooleanField(default=False)
    codedPassword = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Do not enter anything in this field. Will be overwritten by the microsoft API for security purposes.",
    )

    def staffTitle(self):
        if self.title != "":
            return self.title
        return self.rank

    def userProfileName(self):
        if self.usernameAs == "0":
            return "%s@staff.furrydelphia.org" % (slugify(self.fanName).lower())
        if self.usernameAs == "1":
            return "%s%s@staff.furrydelphia.org" % (
                slugify(self.firstName[0]).lower(),
                slugify(self.lastName).lower(),
            )
        if self.usernameAs == "2":
            return "%s%s@staff.furrydelphia.org" % (
                slugify(self.fanName[0]).lower(),
                slugify(self.lastName).lower(),
            )

    def displayName(self):
        if self.displayNameAs == "0":
            return "%s %s" % (self.firstName, self.lastName)
        if self.displayNameAs == "1":
            return "%s %s" % (self.fanName, self.lastName)
        if self.displayNameAs == "2":
            return "%s" % (self.fanName)

    class Meta:
        permissions = [
            ("can_see_hr", "Can see the HR Portal")
        ]
