from django.db import models

import random
# Create your models here.

def genRandNum():
    return "%04d" % random.randint(1,99999)

class Area(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('furry.Profile', on_delete=models.SET_NULL, blank=True, null=True)
    address1 = models.CharField(blank=True, null=True, max_length=100)
    address2 = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    phone_number = models.CharField(blank=True, null=True, max_length=100)
    email = models.CharField(blank=True, null=True, max_length=100)
    access_codes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class Asset(models.Model):

    TYPES = (
        ("AP", "Access Point"),
        ("BX", "Box"),
        ("CA", "Card Printer"),
        ("CH", "Chromebook"),
        ("CP", "Computer"),
        ("LO", "Loaned Hardware"),
        ("MN", "Monitor"),
        ("OT", "Other"),
        ("PR", "Traditional Printer"),
        ("PH", "Phone"),
        ("RD", "Radio"),
        ("RT", "Router"),
        ("SV", "Server"),
        ("SW", "Networking Switch"),
        ("TB", "Tablet"),
    )

    OWNER = (
        ("FDL", "Furrydelphia, Inc."),
    )

    STATUSES = (
        ("danger", "Checked In - Stored"),
        ("warning", "Checked Out - On Long Term Loan"),
        ("primary", "Checked In - Ready for Use"),
        ("secondary", "In Transit - Transporting"),
        ("success", "Checked Out - In Use"),
        ("dark", "Decommissioned")
    )

    tag = models.CharField(unique=True,primary_key=True,default=genRandNum,max_length=5)
    type = models.CharField(max_length=2, choices=TYPES)
    company = models.CharField(max_length=3, choices=OWNER, default="FDL")
    description = models.CharField(max_length=250)
    serial_number = models.CharField(max_length=100,blank=True,null=True)
    owner = models.EmailField(max_length=100, blank=True, null=True)
    is_convention_owned = models.BooleanField(default=True)
    cost = models.IntegerField(blank=True, null=True)

    box = models.ForeignKey('inventory.Asset', blank=True, null=True, on_delete=models.SET_NULL)

    checked_out_to = models.CharField(max_length=100, blank=True, null=True)
    checked_out_date = models.DateTimeField(blank=True, null=True)
    check_out_department = models.CharField(max_length=100, blank=True, null=True)
    check_out_notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=15, choices=STATUSES, default="primary")

    storage_location = models.ForeignKey('inventory.Area', on_delete=models.SET_NULL, blank=True, null=True)

    def constructAssetTag(self):
        return "%s%s%s" % (self.company, self.tag, self.type)

    def getComments(self):
        kn = []
        for x in AssetLog.objects.filter(asset=self):
            kn.append({
                "user": x.user,
                "date_entered": x.date_entered,
                "entry": x.entry
            })
        return kn


class AssetLog(models.Model):
    asset = models.ForeignKey('inventory.Asset', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    user_match = models.ForeignKey('furry.Profile', on_delete=models.SET_NULL, blank=True, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    entry = models.TextField()