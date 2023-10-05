from django.db import models
from django.contrib import admin
from decimal import Decimal
from django.core.exceptions import ValidationError
import uuid,datetime

class RegistrantLevel(models.Model):
    level_id = models.TextField(max_length=200,verbose_name='Level ID')
    label = models.TextField(max_length=200,verbose_name='Level Label')
    active = models.BooleanField(verbose_name="Level Active Flag",default=True)
    cost = models.IntegerField(verbose_name='Cost',default=65)
    stripe_price = models.TextField(max_length=200,verbose_name='Level Stripe Price ID')
    stripe_price_test = models.TextField(max_length=200,verbose_name='Level Stripe Test Price ID')
    def __str__(self):
        return f'{self.label} (${self.cost})'


@admin.register(RegistrantLevel)
class RegistrantLevelAdmin(admin.ModelAdmin):
    pass


# Create your models here.
class Registrant(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    firstName = models.CharField(max_length=100,verbose_name="First Name: ")
    lastName = models.CharField(max_length=100,verbose_name="Last Name: ")
    email = models.CharField(max_length=100,verbose_name="Email: ")
    phone = models.CharField(max_length=20,verbose_name="Phone #: ")
    addr1 = models.CharField(max_length=100,verbose_name="Address Line 1: ")
    addr2 = models.CharField(max_length=100,verbose_name="Address Line 2: ",blank=True)
    country = models.CharField(max_length=100,verbose_name="Country: ")
    city = models.CharField(max_length=100,verbose_name="City: ")
    state = models.CharField(max_length=10,verbose_name="State/Province: ")
    zip = models.CharField(max_length=10,verbose_name="Address Zip/Post Code: ")
    dob = models.DateField(verbose_name="Date of Birth: ")
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created: ')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated: ')
    level = models.ForeignKey(RegistrantLevel,verbose_name="Registrant Level: ",on_delete=models.RESTRICT)
    profile = models.ForeignKey('furry.Profile',verbose_name="Registrant Profile: ",on_delete=models.RESTRICT,blank=True,null=True)
    fdDonation =  models.DecimalField(verbose_name='Furrydelphia Donation: ',default=0,max_digits=10,decimal_places=2)
    chDonation =  models.DecimalField(verbose_name='Charity Donation: ',default=0,max_digits=10,decimal_places=2)
    badgeName = models.CharField(max_length=100,verbose_name="Badge Name: ")
    agreeCOC = models.BooleanField(verbose_name="Agreed to Code of Conduct",default=False,blank=False)
    agreeCOCDate = models.DateTimeField(verbose_name="Agreed to Code of Conduct Date",blank=True,null=True)
    agreeRFP = models.BooleanField(verbose_name=" Agreed Refund Policy",default=False)
    agreeRFPDate = models.DateTimeField(verbose_name="Agreed to Refund Policy Date",blank=True,null=True)
    agreeCVD = models.BooleanField(verbose_name=" Agreed to the COVID Policy",default=False)
    agreeCVDDate = models.DateTimeField(verbose_name="Agreed to COVID Policy Date",blank=True,null=True)
    paid = models.BooleanField(verbose_name="Paid",default=False)
    paidDate = models.DateTimeField(verbose_name="Payment Date",blank=True,null=True)
    total = models.CharField(max_length=100, verbose_name="Total",blank=True, null=True)
    amount = models.CharField(max_length=100,verbose_name="Amount", blank=True, null=True)
    outstandingAmount = models.CharField(max_length=100, verbose_name="Outstanding Amount",blank=True, null=True)
    currency = models.CharField(max_length=3,verbose_name="Currency",default="USD", blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.dob < datetime.date(1923,1,1):
            raise ValidationError("Are you really that old?")
        super(Registrant, self).save(*args, **kwargs)

    def __str__(self):
        if self.paid == True:
            return f'{self.uuid}: {self.firstName} {self.lastName} **PAID**'
        else:
            return f'{self.uuid}: {self.firstName} {self.lastName} **UNPAID**'
@admin.register(Registrant)
class RegistrantAdmin(admin.ModelAdmin):
    pass
