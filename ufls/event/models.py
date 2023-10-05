import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Location(models.Model):
    event = models.ForeignKey('registration.Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    space_name = models.CharField(max_length=100, help_text="Name in physical location")

class HotTable(models.Model):
    day = (
        ("F", "Friday"),
        ("S", "Saturday")
    )

    dealer = models.ForeignKey('marketplace.Dealer', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    selected_day = models.CharField(choices=day, max_length=1, default="F")
    event = models.ForeignKey('registration.Event', on_delete=models.CASCADE)
    intended_selling = models.TextField(default="", help_text="What do you intend on selling at your Hot Table? This can be anything from normal wares to specialized, 18+ items/art/clothing/etc.")


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

