from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError
import uuid,datetime
import datetime
from communities.profiles.models import Profile
from communities.community.models import Community
from ufls.event.models import Event



class Application(models.Model):
    class Meta:
        db_table = "ufls_registrar_application"
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    questions = models.JSONField(default=[])
    openDate = models.DateTimeField(default=datetime.datetime.now)
    closeDate = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField()
    showOnSidebar = models.BooleanField(default=True, help_text="Shows on Dashboard Sidebar as an Application to submit for")
    showOnHomepage = models.BooleanField(default=True, help_text="Shows to Guests before login on the Homepage.")
    showOnDashboard = models.BooleanField(default=True, help_text="Shows on the dashboard submission tracker on the right-hand side.")
    departmentBelong = models.ForeignKey('furry.Department', blank=True, null=True, help_text="If not set, will only be seeable by administrators.", on_delete=models.CASCADE)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass

class ApplicationSubmission(models.Model):

    class Meta:
        db_table = "ufls_registrar_application_sumbmission"

    DISPOSITIONS = (
        ("Submitted", "Submitted"),
        ("Under Review", "Under Review"),
        ("Declined", "Declined"),
        ("Approved", "Approved")
    )

    app = models.ForeignKey(Application, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    submission_details = models.JSONField(default=[])
    dateEntered = models.DateTimeField(auto_now_add=True)
    disposition = models.CharField(choices=DISPOSITIONS, default="Submitted", max_length=20)

@admin.register(ApplicationSubmission)
class ApplicationSubmissionAdmin(admin.ModelAdmin):
    pass


class RegistrantLevel(models.Model):
    class Meta:
        db_table = "ufls_registrar_registrant_level"
    uuid =  models.UUIDField(primary_key=True,default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    level_id = models.TextField(max_length=200,verbose_name='Level ID')
    label = models.TextField(max_length=200,verbose_name='Level Label')
    active = models.BooleanField(verbose_name="Level Active Flag",default=True)
    minor = models.BooleanField(verbose_name="Minor Flag", default=True)
    day_pass = models.BooleanField(verbose_name="Day Pass Flag", default=True)
    cost = models.DecimalField(verbose_name='Level Cost',default=65,max_digits=10,decimal_places=2)
    sold = models.IntegerField(verbose_name='Current Count Sold', default=0)
    max = models.IntegerField(verbose_name='Max Sellable Count', default=1000)
    limit_to_max_sales = models.BooleanField(verbose_name="Limit sales to specified max ticket #",default=False)
    stripe_price = models.TextField(max_length=200,verbose_name='Level Stripe Price ID')
    stripe_price_test = models.TextField(max_length=200,verbose_name='Level Stripe Test Price ID')
    def __str__(self):
        return f'{self.label} (${self.cost})'

@admin.register(RegistrantLevel)
class RegistrantLevelAdmin(admin.ModelAdmin):
    pass

class RegistrationLoot(models.Model):
    class Meta:
        db_table = "ufls_registrar_registration_loot"

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    level_id = models.TextField(max_length=200,verbose_name='Loot ID')
    label = models.TextField(max_length=200,verbose_name='Loot Label')
    descr = models.TextField(verbose_name='Loot Description')
    active = models.BooleanField(verbose_name="Loot Active Flag",default=True)
    picture = models.ImageField(verbose_name="Loot Image/Photo", null=True,blank=True)
    purchasable = models.BooleanField(verbose_name="Loot Available for Direct Purchase", default=True)
    customisable = models.BooleanField(verbose_name="Loot Can be Customisable", default=False)
    options = models.JSONField(verbose_name="Customisation options",blank=True,null=True)
    cost = models.FloatField(verbose_name='Loot Cost',default=65)
    sold = models.IntegerField(verbose_name='Current Count Sold', default=0)
    max = models.IntegerField(verbose_name='Max Sellable Count', default=1000)
    limit_to_max_sales = models.BooleanField(verbose_name="Limit sales to specified max count #",default=False)
    stripe_price = models.TextField(max_length=200,verbose_name='Loot Stripe Price ID')
    stripe_price_test = models.TextField(max_length=200,verbose_name='Loot Stripe Test Price ID')
    def __str__(self):
        return f'Registration Loot: {self.label} (${self.cost})'

@admin.register(RegistrationLoot)
class RegistrationLootAdmin(admin.ModelAdmin):
    pass

class RegistrationLevelLoot(models.Model):
    class Meta:
        db_table = "ufls_registrar_registration_level_loot"

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    level = models.ForeignKey(RegistrantLevel,verbose_name='Registration Level',on_delete=models.CASCADE)
    item = models.ForeignKey(RegistrationLoot,verbose_name="Registration Loot Item",on_delete=models.CASCADE)
    cost = models.IntegerField(verbose_name='Loot Cost',default=65)
    count = models.IntegerField(verbose_name='Item Count', default=1)
    active = models.BooleanField(verbose_name="Loot Active Flag",default=True)
    def __str__(self):
        return f'Registration Level Loot: For {self.level.label} Loot item: {self.item.label}'

@admin.register(RegistrationLevelLoot)
class RegistrationLevelLootAdmin(admin.ModelAdmin):
    pass

# Create your models here.
class Registrant(models.Model):
    class Meta:
        db_table = "ufls_registrar_registrant"
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
    event = models.ForeignKey(Event,verbose_name="Registrant Event:",on_delete=models.RESTRICT,null=True)
    profile = models.ForeignKey(Profile,verbose_name="Select profile: ",on_delete=models.RESTRICT,blank=True,null=True)
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

def upload_path_image(instance, filename):
    return '2024av/%s/%s' % (instance.displayId, filename)

def upload_cropped_image_path(instance, filename):
    return '2024/coppedphotos/%s/%s' % (instance.displayId, filename)

class RegistrantData(models.Model):
    class Meta:
        db_table = "ufls_registrar_registrant_data"
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
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
    conRegLevel = models.ForeignKey(RegistrantLevel, blank=True, null=True, on_delete=models.SET_NULL)
    vetoBadgePic = models.BooleanField(default=False)
    isForwarding = models.BooleanField(default=False)
    generatedViaWebhook = models.BooleanField(default=False)

    accessibility = models.BooleanField(default=False)

    a11yPartialAssist = models.BooleanField(default=False)
    a11yFullAssist = models.BooleanField(default=False)
    a11yEyesight = models.BooleanField(default=False)
    a11yChair = models.BooleanField(default=False)
    a11yElevator = models.BooleanField(default=False)
    a11yGroup = models.BooleanField(default=False)
    a11yNotes = models.TextField(blank=True, null=True)
    a11yEvents = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Registrant Data {self.pk}: {self.conFirstName} {self.conLastName}, {self.conRegLevel}"
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

@admin.register(RegistrantData)
class RegistrantDataAdmin(admin.ModelAdmin):
    pass


class Badge(models.Model):
    class Meta:
        db_table = "ufls_registrar_badge"
    registrant = models.ForeignKey(RegistrantData, on_delete=models.CASCADE)
    number = models.CharField(max_length=50, default="NEW")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    def save(self, *args, **kwargs):
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


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    pass



class PrintJob(models.Model):
    class Meta:
        db_table = "ufls_registrar_print_job"
    screenData = models.JSONField(blank=True,null=True)
    resolved = models.BooleanField(default=False)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeCompleted = models.DateTimeField(auto_now=True)
    handling = models.BooleanField(default=False)

@admin.register(PrintJob)
class PrintJobAdmin(admin.ModelAdmin):
    pass


class RegistrarLevelLootView(models.Model):
    class Meta:
        managed = False
        db_table = "ufls_registrar_level_loot_view"
    #level_id = models.UUIDField(verbose_name="Level UUID")
    level = models.ForeignKey(RegistrantLevel,on_delete=models.CASCADE,related_name="+")
    loot = models.ForeignKey(RegistrationLoot,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name="Loot ID")
    label = models.TextField(verbose_name="Level Label")
    active = models.BooleanField(verbose_name="Level Active")
    picture = models.ImageField(verbose_name="Loot Image/Photo", null=True, blank=True)
    loot_label = models.TextField(verbose_name="Loot Label")
    loot_active = models.BooleanField(verbose_name="Loot Active")
    cost = models.DecimalField(verbose_name="Loot Cost",max_digits=10,decimal_places=2)
    purchasable = models.BooleanField(verbose_name="Loot Purchasable")
    descr = models.TextField(verbose_name="Loot Descr")
    count = models.PositiveIntegerField(verbose_name="Loot Count",default=1)

class RegistrantLootFulfillment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name="Fulfilment Request ID")
    registrant = models.ForeignKey(Registrant,on_delete=models.CASCADE,verbose_name="Registrant")
    loot = models.ForeignKey(RegistrationLoot,on_delete=models.CASCADE,verbose_name="Loot Type")
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="Item Count",default=1)
    active = models.BooleanField(verbose_name="Fulfilment Request Active",default=False)
    fulfilled = models.BooleanField(verbose_name="Request Complete",default=False)
    created = models.DateTimeField(verbose_name="Request Created",auto_now_add=True)
    fulfilled_on = models.DateTimeField(verbose_name="Request Fulfilled on",blank=True,null=True)
    remarks = models.TextField(verbose_name="Request Remarks",blank=True,null=True)
    def __str__(self):
        return f"Event->Registrant Loot Fulfilment: {self.event.name}, Reg: {self.registrant}, Loot: {self.loot}, Count: {self.count}"
@admin.register(RegistrantLootFulfillment)
class RegistrantLootFulfillmentAdmin(admin.ModelAdmin):
        pass