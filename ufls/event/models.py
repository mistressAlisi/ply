import uuid
import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
from communities.community.models import Community
# Create your models here.


class Event(models.Model):
    class Meta:
        db_table = "ufls_event_event"
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=100,verbose_name="Event Name",help_text="Will be displayed EVERYWHERE.")
    active = models.BooleanField(default=False,verbose_name="Event Active",help_text="Enable/open Event")
    #timeLastSync = models.DateTimeField(blank=True,null=True)
    isSecAccessEnabled = models.BooleanField(default=False, help_text="Enables the PocketSec application to be used by PSafe",verbose_name="Enable PSafe")
    # TODO: move to their own model.
    # uniqueBadgeNumbers = models.IntegerField(default=1)
    # uniqueBadgeNumbersCard = models.IntegerField(default=100)
    # banList = models.TextField(blank=True, null=True, help_text="Enter a First/Last name, or known Con Badge Name. One entry per line. Security will be notified if this name is detected.")
    startDate = models.DateField(blank=True,null=True,verbose_name="Start Date",help_text="Event Start Date")
    endDate = models.DateField(blank=True, null=True,verbose_name="End Date",help_text="Event End Date")
    regOpen = models.DateTimeField(verbose_name="Registration Open",help_text="Date registration opens")
    regClose = models.DateTimeField(verbose_name="Registration Close",help_text="Date registration closes")
    #regEditOpen = models.DateTimeField(verbose_name="Registration Editing Period Open",help_text="Start of period during which registration edits are allowed")
    #regEditClose = models.DateTimeField(verbose_name="Registration Editing Period Close",help_text="End of period during which registration edits are allowed")
    # advanced forms
    dealersOpen = models.DateTimeField(verbose_name="Dealers Den Open",help_text="Start of Dealers' den being open")
    dealersClose = models.DateTimeField(verbose_name="Dealers Den Close",help_text="End of Dealers' den being open")
    aaOpen = models.DateTimeField(verbose_name="Applications Accepted Open",help_text="Start of Applications Period")
    aaClose = models.DateTimeField(verbose_name="Applications Accepted Close",help_text="End of Applications Period")
    eventsOpen = models.DateTimeField(verbose_name="Events Open",help_text="Start of Events Period")
    eventsClose = models.DateTimeField(verbose_name="Events Close",help_text="End of Events Period")
    eventAppCode = models.CharField(max_length=100)
    def __str__(self):
        return f"Event: {self.name}"
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


class EventCommunityMapping(models.Model):
    class Meta:
        db_table = "ufls_event_event_community_mapping"
        unique_together = ["event","community"]
    uuid = models.UUIDField(default=uuid.uuid4,primary_key=True)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE,null=True)
    active = models.BooleanField(verbose_name="Active",default=True)

    def __str__(self):
        return f"Event->Community Mapping: {self.event.name}->{self.community.name}"

@admin.register(EventCommunityMapping)
class EventCommunityMappingAdmin(admin.ModelAdmin):
        pass

class Location(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    space_name = models.CharField(max_length=100, help_text="Name in physical location")

# class HotTable(models.Model):
#     day = (
#         ("F", "Friday"),
#         ("S", "Saturday")
#     )
#
#     dealer = models.ForeignKey('marketplace.Dealer', on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#     confirmed = models.BooleanField(default=False)
#     selected_day = models.CharField(choices=day, max_length=1, default="F")
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#    intended_selling = models.TextField(default="", help_text="What do you intend on selling at your Hot Table? This can be anything from normal wares to specialized, 18+ items/art/clothing/etc.")


class Invoice(models.Model):

    TYPES = (
        ("reg", "Registration Invoice"),
        ("table", "Table Invoice"),
        ("general", "General Invoice"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(choices=TYPES, default="general", max_length=20)
    description = models.CharField(max_length=50)
    square_code = models.CharField(max_length=100,blank=True,null=True)
    amount_collected = models.CharField(max_length=100,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_paid = models.DateTimeField(blank=True,null=True)
    date_due = models.DateTimeField(blank=True,null=True)
    reference_id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True)
    checkout_id = models.CharField(max_length=250,blank=True,null=True)
    idempotency_key = models.UUIDField(default=uuid.uuid4)
    debug_result_data = models.JSONField(default=dict)
    # data schema
    """
        {
        "item_map": ["l1","l2","l3","l4","l5"],
        "item_details": {
                "l1": {
                    "title"
                    "price"
                    "qty"
                    "discounts": [["discount_percentage","Discount_Percentage_Text"]]
                },
                "l2": ...
            },
        "taxes": [["tax_percentage","tax_percentage_text"]]
        "admin_notes": "",
        }

    """

