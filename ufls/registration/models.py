import json
import os
import random
import string

import urllib3
from decouple import config
from django.contrib.auth import get_user_model
from django.db import models
from datetime import date, datetime
from django.utils import timezone


# Create your models here.

class Event(models.Model):
    class Meta:
        db_table = "ufls_"
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    regfoxPageCode = models.CharField(max_length=100)
    regfoxStaffPageCode = models.CharField(max_length=100, blank=True, null=True)
    timeLastSync = models.DateTimeField(blank=True,null=True)
    isSecAccessEnabled = models.BooleanField(default=False, help_text="Enables the PocketSec application to be used by PSafe")
    uniqueBadgeNumbers = models.IntegerField(default=1)
    uniqueBadgeNumbersCard = models.IntegerField(default=100)
    banList = models.TextField(blank=True, null=True, help_text="Enter a First/Last name, or known Con Badge Name. One entry per line. Security will be notified if this name is detected.")
    startDate = models.DateField(blank=True,null=True)
    endDate = models.DateField(blank=True, null=True)
    regOpen = models.DateTimeField(default=timezone.now())
    regClose = models.DateTimeField(default=timezone.now())
    regEditOpen = models.DateTimeField(default=timezone.now())
    regEditClose = models.DateTimeField(default=timezone.now())
    # advanced forms
    dealersOpen = models.DateTimeField(default=timezone.now())
    dealersClose = models.DateTimeField(default=timezone.now())
    aaOpen = models.DateTimeField(default=timezone.now())
    aaClose = models.DateTimeField(default=timezone.now())
    eventsOpen = models.DateTimeField(default=timezone.now())
    eventsClose = models.DateTimeField(default=timezone.now())
    eventAppCode = models.CharField(max_length=100)

class Application(models.Model):
    event = models.ForeignKey('registration.Event', on_delete=models.CASCADE)
    questions = models.JSONField(default=[])
    openDate = models.DateTimeField(default=timezone.now())
    closeDate = models.DateTimeField(default=timezone.now())
    description = models.TextField()
    showOnSidebar = models.BooleanField(default=True, help_text="Shows on Dashboard Sidebar as an Application to submit for")
    showOnHomepage = models.BooleanField(default=True, help_text="Shows to Guests before login on the Homepage.")
    showOnDashboard = models.BooleanField(default=True, help_text="Shows on the dashboard submission tracker on the right-hand side.")
    departmentBelong = models.ForeignKey('furry.Department', blank=True, null=True, help_text="If not set, will only be seeable by administrators.", on_delete=models.CASCADE)

class ApplicationSubmission(models.Model):

    DISPOSITIONS = (
        ("Submitted", "Submitted"),
        ("Under Review", "Under Review"),
        ("Declined", "Declined"),
        ("Approved", "Approved")
    )

    app = models.ForeignKey('registration.Application', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    submission_details = models.JSONField(default=[])
    dateEntered = models.DateTimeField(auto_now_add=True)
    disposition = models.CharField(choices=DISPOSITIONS, default="Submitted", max_length=20)


# FIXME: @YUUKI WTF?: Why is this here?!?!
def upload_path_image(instance, filename):
    return '2022av/%s/%s' % (instance.displayId, filename)
# FIXME: @YUUKI WTF?: Why is this here?!?!
def upload_cropped_image_path(instance, filename):
    return '2022croppedphotos/%s/%s' % (instance.displayId, filename)


class StringKeyGenerator(object):
    def __init__(self, len=64):
        self.lenght = len
    def __call__(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(self.lenght))
    def salt(self):
        return ''.join(random.choice(string.ascii_uppercase) for x in range(self.lenght))

class WebconnexAction(models.Model):

    TYPES = (
        ("registration", "New Registration"),
        ("registrant_edit", "Registration Modification from Regfox"),
    )

    id = models.CharField(max_length=64, unique=True, primary_key=True, default=StringKeyGenerator().__call__)
    raw_data = models.JSONField(blank=True, null=True)
    _type = models.CharField(choices=TYPES, max_length=100, blank=True, null=True)
    acted_upon = models.BooleanField(default=False)
    def updateAttachedRegistrant(self):
        http = urllib3.PoolManager()
        apikey = config("UFLS_REGFOX_API_KEY", default="")
        cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default=os.environ.get('CURRENT_EVENT_PK'))

        event = Event.objects.get(pk=cur_event_pk)
        for reg in self.raw_data['data']['registrants']:
            r = http.request('GET',
                             'https://api.webconnex.com/v2/public/search/registrants/%s?product=regfox.com&pretty=false' % (
                             reg['lookupId']), headers={"apiKey": apikey})

            incomingData = json.loads(r.data.decode('utf-8'))
            x = incomingData['data']
            if (x['status'] == "pending-CHANGEMETODO"):
                pass
                # print("Skipping Pending Transaction")
            else:
                lkp = RegistrantData.objects.filter(formId=x['formId'], rId=x['id'], displayId=x['displayId']).first()
                if (lkp == None):
                    lkp = RegistrantData.objects.create(
                        event=event,
                        rId=x['id'],
                        displayId=x['displayId'],
                        formId=x['formId'],
                        formName=x['formName'],
                        formAccRef=x['formAccRef'],
                        orderCustomerId=x['orderCustomerId'],
                        customerId=x['customerId'],
                        orderId=x['orderId'],
                        orderDisplayId=x['orderDisplayId'],
                        orderNumber=x['orderNumber'],
                        orderEmail=x['orderEmail'],
                        status=x['status'],
                        total=x['total'],
                        amount=x['amount'],
                        outstandingAmount=x['outstandingAmount'],
                        currency=x['currency'],
                        fieldData=x['fieldData'],
                        metadata=x['metadata'],
                        checkedIn=x['checkedIn'],
                        dateCreated=x['dateCreated'],
                    )
                    # try:
                    #    lkp.dateUpdated = x['dateUpdated']
                    # except KeyError:
                    #    print("Could not update dateUpdated for %s" % lkp.pk)
                    #    pass
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2023STAFF":
                                lkp.conIsStaff = True
                            if y['value'].find("DEALER") != -1:
                                lkp.conIsDealer = True
                            if y['value'].find("-A") != -1:
                                lkp.conIsDealerAssistant = True
                        if (y['path'] == "yourLegalName.first"):
                            lkp.conFirstName = y['value']
                        if (y['path'] == "yourLegalName.last"):
                            lkp.conLastName = y['value']
                        if (y['path'] == "email"):
                            lkp.conEmail = y['value'].lower()
                        if (y['path'] == "badgeName"):
                            lkp.conBadgeName = y['value']
                        if (y['path'] == "products.mealPlan"):
                            if y['value'] == "1":
                                lkp.hasMealPlan = True
                        if (y['path'] == "dateOfBirth"):
                            lkp.conDOB = y['value']
                        if (y['path'] == "registrationOptions"):
                            lkp.conRegLevel = ConBadgeLevelMap.objects.filter(event=event,
                                                                              regfoxValue=y['value']).first()
                else:
                    lkp.rId = x['id']
                    lkp.displayId = x['displayId']
                    lkp.formId = x['formId']
                    lkp.formName = x['formName']
                    lkp.formAccRef = x['formAccRef']
                    lkp.orderCustomerId = x['orderCustomerId']
                    lkp.customerId = x['customerId']
                    lkp.orderId = x['orderId']
                    lkp.orderDisplayId = x['orderDisplayId']
                    lkp.orderNumber = x['orderNumber']
                    lkp.orderEmail = x['orderEmail']
                    lkp.status = x['status']
                    lkp.total = x['total']
                    lkp.amount = x['amount']
                    lkp.outstandingAmount = x['outstandingAmount']
                    lkp.currency = x['currency']
                    lkp.fieldData = x['fieldData']
                    lkp.metadata = x['metadata']
                    lkp.checkedIn = x['checkedIn']
                    lkp.dateCreated = x['dateCreated']
                    # lkp.dateUpdated=x['dateUpdated']
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2023STAFF":
                                lkp.conIsStaff = True
                            if y['value'].find("DEALER") != -1:
                                lkp.conIsDealer = True
                            if y['value'].find("-A") != -1:
                                lkp.conIsDealerAssistant = True
                        if (y['path'] == "yourLegalName.first"):
                            lkp.conFirstName = y['value']
                        if (y['path'] == "yourLegalName.last"):
                            lkp.conLastName = y['value']
                        if (y['path'] == "email"):
                            lkp.conEmail = y['value'].lower()
                        if (y['path'] == "badgeName"):
                            lkp.conBadgeName = y['value']
                        if (y['path'] == "products.mealPlan"):
                            if y['value'] == "1":
                                lkp.hasMealPlan = True
                        if (y['path'] == "dateOfBirth"):
                            lkp.conDOB = y['value']
                        if (y['path'] == "registrationOptions"):
                            lkp.conRegLevel = ConBadgeLevelMap.objects.filter(event=event,
                                                                              regfoxValue=y['value']).first()
                lkp.regfox_webhook = self
                lkp.generatedViaWebhook = True
                lkp.save()
                self.acted_upon = True
                self.save()
                # print("Registrant Updated: " + lkp.displayId)

class RegistrantData(models.Model):
    account = models.ForeignKey('furry.Profile', blank=True, null=True, on_delete=models.SET_NULL)
    isCustomPicture = models.BooleanField(default=False)
    customUploadPicture = models.ImageField(upload_to=upload_path_image, blank=True, null=True)
    croppedImage = models.ImageField(upload_to=upload_cropped_image_path, blank=True, null=True)
    event = models.ForeignKey('registration.Event', on_delete=models.PROTECT)
    rId = models.CharField(max_length=50, help_text="Regfox ID", blank=True, null=True)
    rUUID = models.UUIDField(help_text="Internal Registrar UUID", blank=True, null=True)
    displayId = models.CharField(max_length=100,blank=True, null=True)
    formId = models.CharField(max_length=100,blank=True, null=True)
    formName = models.CharField(max_length=100,blank=True, null=True)
    formAccRef = models.CharField(max_length=100,blank=True, null=True)
    orderCustomerId = models.CharField(max_length=100,blank=True, null=True)
    customerId = models.CharField(max_length=100, blank=True, null=True)
    orderId = models.CharField(max_length=100, blank=True, null=True)
    orderDisplayId = models.CharField(max_length=100, blank=True, null=True)
    orderNumber = models.CharField(max_length=100, blank=True, null=True)
    orderEmail = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    outstandingAmount = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    fieldData = models.JSONField(blank=True,null=True)
    metadata = models.CharField(max_length=100, blank=True, null=True)
    checkedIn = models.BooleanField(default=False)
    dateCreated = models.CharField(max_length=100, blank=True, null=True)
    dateUpdated = models.CharField(max_length=100, blank=True, null=True)
    conCheckedIn = models.BooleanField(default=False)
    conCheckedInDate = models.DateTimeField(blank=True,null=True)
    conCreepFlag = models.BooleanField(default=False)
    conBanFlag = models.BooleanField(default=False)
    conRegNotes = models.TextField(blank=True, null=True)
    conBadgeNumber = models.CharField(max_length=100, blank=True, null=True)
    conFirstName = models.CharField(max_length=100, blank=True, null=True)
    conLastName = models.CharField(max_length=100, blank=True, null=True)
    conEmail = models.CharField(max_length=100, blank=True, null=True)
    conDOB = models.CharField(max_length=100, blank=True, null=True)
    conBadgeName = models.CharField(max_length=100, blank=True, null=True)
    conIsStaff = models.BooleanField(default=False)
    conIsDealer = models.BooleanField(default=False)
    conIsDealerAssistant = models.BooleanField(default=False)
    conStaffDepartment = models.CharField(max_length=100, blank=True, null=True)
    conCustomBadgeLevel = models.CharField(max_length=100, blank=True, null=True)
    hasMealPlan = models.BooleanField(default=False)
    conRegLevel = models.ForeignKey('registration.ConBadgeLevelMap', blank=True, null=True, on_delete=models.SET_NULL)
    vetoBadgePic = models.BooleanField(default=False)
    isForwarding = models.BooleanField(default=False)
    generatedViaWebhook = models.BooleanField(default=False)
    regfox_webhook = models.ForeignKey('registration.WebconnexAction', on_delete=models.SET_NULL, blank=True, null=True)
    webhook_cart = models.JSONField(default={}, blank=True, null=True)

    accessibility = models.BooleanField(default=False)

    a11yPartialAssist = models.BooleanField(default=False)
    a11yFullAssist = models.BooleanField(default=False)
    a11yEyesight = models.BooleanField(default=False)
    a11yChair = models.BooleanField(default=False)
    a11yElevator = models.BooleanField(default=False)
    a11yGroup = models.BooleanField(default=False)
    a11yNotes = models.TextField(blank=True, null=True)
    a11yEvents = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(RegistrantData, self).save(*args, **kwargs)
        if(self.conBadgeNumber != None):
            # this is a custom number.
            b = Badge.objects.create(
                number=self.conBadgeNumber,
                event=self.event,
                registrant=self
            )
            b.save()

    def isCardBadge(self):
        if self.conCustomBadgeLevel != None:
            return False
        if self.determineAge() == 14:
            return True
        if self.determineAge() == 15:
            return True
        return self.conRegLevel.badgeIsCard

    def determineBadgeLevel(self):
        if self.conIsStaff:
            return "Staff"
        if self.conIsDealer:
            return "Dealer"
        #if self.conIsDealerAssistant:
            #return "Dealer Assistant"
        if self.conCustomBadgeLevel != None:
            return self.conCustomBadgeLevel
        if self.determineAge() == 14:
            return "**CHILD** - %s" % self.conRegLevel.badgeLevel
        if self.determineAge() == 15:
            return "MINOR - %s" % self.conRegLevel.badgeLevel
        return self.conRegLevel.badgeLevel

    # obsoleted
    def determineImageUrl(self):
        if(self.vetoBadgePic == True or self.displayImageUrl() == "Error"):
            return "https://backend.furrydelphia.org/static/generic.jpeg"
        return self.croppedImage.url

    #obsoleted
    def determineTwentyTwoShip(self):
        valuePath = ""
        for x in self.fieldData:
            if x['path'] == "galacticNavyDepartment":
                valuePath = x['value']
                if(valuePath == ""):
                    return None
                return valuePath
        return None

    # obsoleted
    def determineTwentyTwoShipName(self):
        valuePath = ""
        for x in self.fieldData:
            if x['path'] == "shipName":
                valuePath = x['value']
                if(valuePath == ""):
                    return None
                return valuePath
        return None

    # obsoleted
    def determineFuckery(self, shipName):
        if(shipName.split(" ")[0].lower() == "the"):
            return shipName
        return "the %s" % shipName

    # obsoleted
    def determineDeptOrShipName(self):
        if (self.conRegLevel.regfoxValue == "eliteSponsor"):
            return "Captain of %s" % (self.determineFuckery(self.determineTwentyTwoShipName()))
        if (self.determineTwentyTwoShip() == '' or self.determineTwentyTwoShip() == None):
            # for 2022, return a OPER badge art.
            if(self.conIsStaff):
                return "Fleet Command"
            return "Visitors Pass"

        depts = {
            "communicationsDepartment": "Communications Department",
            "engineeringDepartment": "Engineering Department",
            "flightDepartment": "Flight Department",
            "medicalDepartment": "Medical Department",
            "navigationDepartment": "Navigation Department",
            "operationsDepartment": "Operations Department",
            "scienceDepartment": "Science Department",
            "securityDepartment": "Security Department",
            "tacticalDepartment": "Tactical Department",
            "commandDepartment": "Command Department"
        }

        return depts[self.determineTwentyTwoShip()] or ""

    # obsoleted
    def determineBadgeArtwork(self):
        if(self.conRegLevel.regfoxValue == "eliteSponsor"):
            return "/static/reg/badges/2022/theme/captain.png"
        if(self.determineTwentyTwoShip() == '' or self.determineTwentyTwoShip() == None):
            # for 2022, return a OPER badge art.
            return self.conRegLevel.badgeImageLocation
        return "/static/reg/badges/2022/theme/%s.png" % (self.determineTwentyTwoShip())

    # obsoleted
    def displayImageUrl(self):
        if(self.vetoBadgePic):
            return "https://backend.furrydelphia.org/static/generic.jpeg"
        if(self.isCustomPicture):
            return self.customUploadPicture.url
        valuePath = ""
        for x in self.fieldData:
            if x['path'] == "uploadBadgePicture":
                valuePath = x['value']
                if(valuePath == ""):
                    return "https://backend.furrydelphia.org/static/generic.jpeg"
                return "https://s3.amazonaws.com/uploads.form.webconnex.com/store/%s/%s" % (self.orderDisplayId, valuePath)
        return "Error"


    def mergedName(self):
        return "%s %s" % (self.conFirstName, self.conLastName)

    def getBadge(self):
        b = Badge.objects.filter(registrant=self).first()
        if b == None:
            b = Badge.objects.create(registrant=self)
            b.save()
        return b


    def getBadgeNumber(self):
        b = Badge.objects.filter(registrant=self).first()
        if b == None:
            return None
        return b.number


    def determineAge(self):
        if(self.conDOB == None):
            return None
        d = datetime.strptime(self.conDOB, "%Y-%m-%d").date()
        now = date.today()

        c = now - d

        age = int(c.days / 365)

        if(age >= 18):
            return 18
        elif(age < 18 and age >= 15):
            return 15
        elif(age < 15):
            return 14
        else:
            return 18


#FIXME: @YUUKI... THIS NEEDS TO BE IN CONSTANTS!
exempt_badge_numbers = ["1", "2", "3", "4", "5", "6", "69", "243", "420", "1337"]

class Badge(models.Model):
    registrant = models.ForeignKey('registration.RegistrantData', on_delete=models.CASCADE)
    number = models.CharField(max_length=50, default="NEW")
    event = models.ForeignKey('registration.Event', on_delete=models.SET_NULL, blank=True, null=True)
    def save(self, *args, **kwargs):
        print(self.number)
        ##
        #
        # D = Day Pass
        # M = Minor Pass
        # C = Child-in-tow Pass
        #
        ##
        if self.number == "D" or self.number == "M" or self.number == "C":
            e = Event.objects.filter(pk=self.registrant.event.pk).first()
            findingNumber = False
            activeCount = e.uniqueBadgeNumbersCard
            activeCount += 1
            self.number = self.number + str(activeCount)
            self.event = e
            e.uniqueBadgeNumbersCard = str(activeCount)
            e.save()
            super(Badge, self).save(*args, **kwargs)
        elif self.number == "NEW":
            e = Event.objects.filter(pk=self.registrant.event.pk).first()
            findingNumber = False
            activeCount = e.uniqueBadgeNumbers
            activeCount += 1
            while findingNumber:
                for x in exempt_badge_numbers:
                    if str(activeCount) != x:
                        findingNumber = False
                    else:
                        findingNumber = True
                        activeCount += 1
            self.number = str(activeCount)
            self.event = e
            e.uniqueBadgeNumbers = str(activeCount)
            e.save()
            super(Badge, self).save(*args, **kwargs)
        else:
            super(Badge, self).save(*args, **kwargs)
        #if(self.event == None):
        #    e = Event.objects.filter(pk=self.registrant.event.pk).first()
        #    self.event = e
        ##    e.save()
        #    super(Badge, self).save(*args, **kwargs)




class ConBadgeLevelMap(models.Model):
    event = models.ForeignKey('registration.Event', on_delete=models.CASCADE)
    regfoxPath = models.CharField(max_length=100)
    regfoxValue = models.CharField(max_length=100)
    stripePrice = models.CharField(max_length=200)
    badgeLevel = models.CharField(max_length=100)
    badgeImageLocation = models.CharField(max_length=250)
    badgeHasMerch = models.BooleanField(default=False, help_text="Badge has Merch.")
    badgeIsCard = models.BooleanField(default=False, help_text="Badge is CR80 sized.")
    def __str__(self):
        return "%s / %s" % (self.event.name, self.badgeLevel)

class PrintJob(models.Model):
    screenData = models.JSONField(blank=True,null=True)
    resolved = models.BooleanField(default=False)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeCompleted = models.DateTimeField(auto_now=True)
    handling = models.BooleanField(default=False)
