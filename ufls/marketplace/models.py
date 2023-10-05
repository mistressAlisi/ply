from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField
from slugify import slugify

from event.models import Invoice


class TableSize(models.Model):
    name = models.CharField(max_length=20)
    units = models.IntegerField(help_text="1 unit = 0.5 tables",default=1)
    booth = models.BooleanField(default=False,help_text="check if booth. Unit = 1")
    price = models.CharField(max_length=20)
    assistant_num = models.IntegerField(default=0)
    form_hide = models.BooleanField(default=False, help_text="Hide in the Dealers Application")
    def __str__(self):
        return "%s - $%s, # of Assistants: %s" % (self.name, self.price, self.assistant_num)
    def toSquare(self):
        return self.price.replace(".","")

class ArtistAlley(models.Model):

    CHOICES = (
        ("dig", "Digital Art (prints, comics, badges, etc)"),
        ("tra", "Traditional Art (pencils and markets, paintings, etc)"),
        ("fur", "Fursuit Maker, Accessories, and Prefabs"),
        ("fug", "Fursuit Suiting Supplies & Accessories"),
        ("mus", "Music or Audio"),
        ("bok", "Books / Literature / Published Comics"),
        ("app", "Apparel (shirts, hoodies, bandanas, etc.)"),
        ("acc", "Accessories (harnesses, collars, jewelry, etc)"),
        ("trg", "Traditional Games (board games, card games, etc)"),
        ("vid", "Video Games (games, consoles, accessories, etc.)"),
        ("scu", "Sculptures (figurines, 3D Printed models, etc.)"),
        ("oth", "Other (Unique Items or Services)"),
    )

    AVAIL = (
        ("fri","Friday"),
        ("sat","Saturday"),
        ("sun","Sunday"),
    )

    event = models.ForeignKey('registration.Event', on_delete=models.CASCADE)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    read_rules = models.BooleanField(default=False,blank=True,null=True,verbose_name="Please indicate if you have read and agree to the Artist Alley Rules.")
    first_name = models.CharField(max_length=50,verbose_name="Legal First Name", blank=True, null=True)
    last_name = models.CharField(max_length=50,verbose_name="Legal Last Name", blank=True, null=True)
    preferred_name = models.CharField(max_length=50,verbose_name="Legal Last Name", blank=True, null=True)
    pronouns = models.CharField(max_length=50,verbose_name="Legal Last Name", blank=True, null=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=25,help_text="Furrydelphia will only contact you via phone in the event of an emergency.")
    website = models.CharField(max_length=200,help_text="Where can we see a gallery of examples of your work?")
    table_name = models.CharField(max_length=180,help_text="Example: \"Mr. Ardvark's Awesome Art\"")
    types_of_wares = models.CharField(choices=CHOICES,max_length=200,help_text="Must Select At Least One")
    availability = MultiSelectField(choices=AVAIL,max_length=200,help_text="Must Select At Least One. You will only receive one day unless we are underbooked.",verbose_name="What Days Will you Be Available?")
    waitlisted = models.BooleanField(blank=True,null=True,default=False,verbose_name="If you don't win, would you like to be waitlisted?", help_text="Individuals on the waitlist are encouraged to bring art supplies and other Artist Alley necessities with them to the con. You never know when someone is going to cancel or be a no-show!")
    assigned_day = models.CharField(choices=AVAIL, max_length=100, blank=True, null=True)


class DealerAssistant(models.Model):
    dealer = models.ForeignKey('marketplace.Dealer', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, help_text="Must match name on ID")
    last_name = models.CharField(max_length=50, help_text="Must match name on ID")
    badge_name = models.CharField(max_length=100, help_text="Name for Assistants Badge")
    phone = models.CharField("Phone Number",max_length=50, help_text="This information will be used in case of an emergency.")
    vegan_opt = models.BooleanField('Vegan?', default=False)
    vegetarian_opt = models.BooleanField('Vegetarian?', default=False)
    rest_food = models.TextField('Any Dietary Restrictions or Food Allergies we should know about?',blank=True,null=True)

class TableDefinition(models.Model):
    map_key = models.ForeignKey("event.Location", on_delete=models.CASCADE)
    coords = models.CharField(max_length=500,blank=True,null=True,help_text="poly imagemap coords, example: x1,y1,x2,y2,x3,y3,...")
    designation = models.CharField(max_length=50,blank=True,null=True)
    polygons = models.JSONField(blank=True, null=True, default=list)

    def color(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                if asn.dealer.open:
                    return "00FF00";
                else:
                    return "18a7ff"
        return "FFFF00"
    def businessName(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                return asn.dealer.business_name
        return "Empty"
    def selling(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                return asn.dealer.get_type_of_wares_display()
        return "Empty"
    def status(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                return asn.dealer.open
        return False

    def tableDescription(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                return asn.dealer.conDescription
        return ""

    def slug(self):
        asn = TableAssignment.objects.filter(table=self).first()
        if asn:
            if asn.dealer != None:
                return asn.dealer.dealer_slug
        return ""
    def __str__(self):
        return "%s / %s" % (self.map_key, self.designation)

class TableAssignment(models.Model):
    dealer = models.ForeignKey("marketplace.Dealer", on_delete=models.CASCADE)
    table = models.ForeignKey("marketplace.TableDefinition", on_delete=models.CASCADE)
    def get_business_name(self):
        return self.dealer.business_name
    def get_table_designation(self):
        return self.table.designation
    def get_dealer_slug(self):
        return self.dealer.dealer_slug

class Dealer(models.Model):

    AREAS = (
        ("D", "Standard (Day) Dealers Den"),
        ("N", "18+ (Night) Dealers Den")
    )
    CHOICES = (
        ("secondary", "Application Submitted - Not Reviewed"),
        ("primary", "Dealer Confirmed, all requirements satisfied"),
        ("warning", "Application Submitted - Need Information"),
        ("danger", "Application Declined"),
        ("info condition", "Application Archived"),
        ("info", "Application Waitlisted"),
        ("success", "Application Approved"),
        ("warning condition", "Application Originally Approved - Waitlisted due to Capacity"),
        ("warning delinquent", "Action Required - Delinquent in Deadlines"),
        ("success hello", "Checked In"),
    )

    WARES = (
        ("dig", "Digital Art (prints, comics, badges, etc)"),
        ("tra", "Traditional Art (pencils and markets, paintings, etc)"),
        ("fur", "Fursuit Maker, Accessories, and Prefabs"),
        ("fug", "Fursuit Suiting Supplies & Accessories"),
        ("mus", "Music or Audio"),
        ("bok", "Books / Literature / Published Comics"),
        ("app", "Apparel (shirts, hoodies, bandanas, etc.)"),
        ("acc", "Accessories (harnesses, collars, jewelry, etc)"),
        ("trg", "Traditional Games (board games, card games, etc)"),
        ("vid", "Video Games (games, consoles, accessories, etc.)"),
        ("scu", "Sculptures (figurines, 3D Printed models, etc.)"),
        ("oth", "Other (Unique Items or Services)"),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    area = models.CharField(choices=AREAS, default='D', max_length=1)
    event = models.ForeignKey('registration.Event',on_delete=models.CASCADE)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    address1 = models.CharField("Address Line 1",max_length=100)
    address2 = models.CharField("Address Line 2",max_length=100,blank=True,null=True)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=10,help_text="The address above should be the address for your business.")
    phone = models.CharField("Phone Number",max_length=50)
    emails_ok = models.BooleanField(default=True,help_text="Can we send you e-mail outside of the reminder and approval status e-mails?")
    survey_ok = models.BooleanField(default=True,help_text="Will you participate in our survey after con?")
    birthdate = models.DateField()

    dealer_slug = models.CharField(max_length=100,blank=True,null=True)

    reg_codes = models.TextField(blank=True,null=True)

    registration_lookup = models.CharField(max_length=150,blank=True,null=True)

    business_name = models.CharField(max_length=250,help_text="Enter your business name as it appears on your Tax License, or as it will appear on your tax license")
    dba_name = models.CharField(max_length=250,blank=True,null=True)
    dba_same = models.BooleanField(default=False)
    qs_business_registration_location = models.CharField(max_length=30,blank=True,null=True)
    qs_license_already_obtained = models.CharField(max_length=30,blank=True,null=True)
    license = models.CharField("License Number",max_length=100,blank=True,null=True,help_text="Enter just your license number as it appears on your Tax License. If you don't have a tax license, put 'None'")
    type_of_wares = models.CharField(max_length=5,choices=WARES,help_text="What will you primarially be selling?")
#	type_of_wares = MultiSelectField(max_length=5,choices=WARES,help_text="What will you primarially be selling?",blank=True,null=True)
    description = models.TextField(blank=True,null=True,help_text="Tell us about your business.")

    table_size = models.ForeignKey('marketplace.TableSize',related_name='table_size', on_delete=models.CASCADE,help_text="Select the size of table you would like to have.")
    backup_table_size = models.ForeignKey('marketplace.TableSize',related_name='backup_table_size', blank=True, null=True, on_delete=models.CASCADE)

    near_to = models.CharField('Preferred Neighbors',max_length=500,help_text="If there is anyone who you would like your table placed next to or close to, please list them here. If they list you on their application form as well, we will do our best to put you together. Furrydelphia cannot guarantee these preferences will be met, but we will certainly try! Make sure anyone that you list in your application, lists you on their application as well!",blank=True,null=True)
    far_from = models.CharField('Bad Neighbors',max_length=500,help_text="If there is anyone you are feuding with who you would like your table placed far away from, please list them here. You don't have to tell us why, just list their names. Furrydelphia cannot guarantee these preferences will be met, but we will certainly try!",blank=True,null=True)
    vegan_opt = models.BooleanField('Vegan?', default=False)
    vegetarian_opt = models.BooleanField('Vegetarian?', default=False)
    rest_food = models.TextField('Any Dietary Restrictions or Food Allergies we should know about?',blank=True,null=True)
    registration_cert = models.BooleanField(help_text="I understand that if I am selected I will have 30 days to Register for Furrydelphia and Pay all Dues or my Acceptance will be Revoked.")
    license_cert = models.BooleanField(help_text="I understand that if I am selected I will have 60 days to apply for a PA Tax License or my Acceptance will be Revoked.")
    website = models.CharField(max_length=500,help_text="This is required, as we need to see what kind of work you will be selling. This can be anything from a professional website to a DeviantArt or FurAffinity Account.")
    terms_cert = models.BooleanField(help_text="I understand and agree to the Furrydelphia Marketplace Terms & Conditions.")
    decided = models.BooleanField(default=False)
    status = models.CharField(choices=CHOICES,default="secondary",max_length=100)
    status_sendalong_notes = models.TextField(blank=True,null=True)
    reason = models.TextField(blank=True,null=True)

    atcon_open = models.BooleanField('Open For Commissions?', default=False, help_text="If checked, your map icon will be marked green as Open for Commissions.")

    paid = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    license_verified = models.BooleanField(default=False)
    contract_signed = models.BooleanField(default=False)

    contract_url = models.CharField(max_length=100, blank=True, null=True)

    admin_notes = models.TextField(blank=True,null=True)


    can_manage_assistants = models.BooleanField(default=False)

    badge_name = models.CharField(max_length=20,blank=True,null=True,help_text="Enter your badge name. For approved Dealers.")
    no_mail = models.BooleanField(default=False, help_text="Does not send any e-mail to this dealer. Note, this will automatically set itself to True if the application is Rejected.")

    table_invoice = models.CharField(max_length=100, blank=True, null=True)

    registration_invoice = models.CharField(max_length=100,blank=True,null=True)

    matchEmail = models.CharField(max_length=100,blank=True,null=True)
    hotelReservationLink = models.CharField(max_length=300,blank=True,null=True)

    freebiesLeft = models.IntegerField(default=3)

    atcon_description = models.CharField('Map and List Description', max_length=250, blank=True, null=True, help_text='This description will show up under your name in the Marketplace App! We recommend you use this space to talk about commissions, what you sell, etc, and change it based on your preferences during the convention to keep attendees up to date!')
    atcon_showContact = models.BooleanField('Show E-mail?', default=False, help_text="Show your contact e-mail to Attendees in the Marketplace App.")
    atcon_showWebsite = models.BooleanField('Show Website?', default=False, help_text="Show your portfolio website to Attendees in the Marketplace App.")
    atcon_showSocialMedia = models.BooleanField('Show Social Media?', default=False, help_text="Show your social media contacts to Attendees in the Marketplace App.")
    atcon_twitter = models.CharField('Twitter', max_length=20, blank=True,null=True, help_text="Write your twitter handle (e.g. @furrydelphia), do not include https://twitter.com/. If you put nothing here, it will be hidden from your page.")
    atcon_facebook = models.CharField('Facebook', max_length=500, blank=True,null=True, help_text="Display your facebook page. If you put nothing here, it will be hidden from your page.")
    atcon_furAffinity = models.CharField('FurAffinity', max_length=500, blank=True,null=True, help_text="Display your FurAffinity page (e.g. https://furaffinity.net/user/furrydelphia). If you put nothing here, it will be hidden from your page.")
    atcon_instagram = models.CharField('Instagram', max_length=500, blank=True,null=True, help_text="Display your Instagram page (e.g. https://instagram.com/furrydelphia) If you put nothing here, it will be hidden from your page.")

    number = models.CharField(blank=True, null=True, max_length=2, default='0')

    upgr_flag = models.BooleanField(default=False, help_text="Using their backup table size, percentage discount applied.")

    __original_status = None
    __original_license_verified = False
    __original_license = None
    class Meta:
        ordering = ('table_size',)

    def __str__(self):
        return "%s [%s]" %  (self.business_name, self.get_status_display())

    def __init__(self, *args, **kwargs):
        super(Dealer, self).__init__(*args, **kwargs)
        self.__original_status = self.status
        self.__original_license_verified = self.license_verified
        self.__original_license = self.license


    def save(self, *args, **kwargs):
        super(Dealer, self).save(*args, **kwargs)

        self.dealer_slug = slugify(self.business_name)
        try:
            if(kwargs['force_insert'] == True):
                kwargs['force_insert'] = False
        except:
            pass
        super(Dealer, self).save(*args, **kwargs)
        # TODO: ADD STUFF BACK HERE BRUH

    def statusText(self):
        if self.status == "secondary":
            return "dark"
        else:
            return "white"
    def invoices(self):
        return Invoice.objects.filter(dealer=self)
    def displayStatus(self):
        if self.status == "success" or self.status == "warning condition":
            tn = self.get_status_display()
            if self.license == "" or self.license == "None" or self.license == None:
                tn += "<li>Need License Number</li>"
            else:
                if self.license_verified != True:
                    tn += "<li>License to be Verified</li>"
            if self.registered != True:
                tn += "<li>Must Register for Furrydelphia</li>"
            if self.paid != True:
                tn += "<li>Must Pay for Table</li>"
            if tn == self.get_status_display():
                tn += "<li>No Further Action Required</li>"
            return tn
        if self.emailVerified() == False:
            return "Not Submitted, Verify E-mail"
        return self.get_status_display()
    def allowedAssistants(self):
        return self.table_size.assistant_num
    def remainingAssistants(self):
        return (self.table_size.assistant_num - DealerAssistant.objects.filter(dealer=self).count())
    def atconEmail(self):
        if(self.showContact):
            return self.account.email
        else:
            return None
    def atconWebsite(self):
        if(self.showWebsite):
            return self.website
        else:
            return None
    def assignedTable(self):
        t = TableAssignment.objects.filter(dealer=self).first()
        if(t == None):
            return "Unassigned"
        return \
            {
                "space_number": t.table.designation,
                "area": t.table.map_key.name,
                "location": t.table.map_key.room_location,
                "den_area": self.area
            }

