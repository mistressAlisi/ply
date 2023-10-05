from django.contrib import admin, messages

from connections.models import ReservationKey
from .models import RegistrantData, ConBadgeLevelMap, Event, PrintJob, Badge, WebconnexAction
from .tasks import syncAllFromRegfox, syncStaffFromRegfox
from celery import current_app
from import_export.admin import ImportExportModelAdmin
import os
from ufls.celery import app as Celery
# Register your models here.
from decouple import config

cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="")

def doRegfoxSync(modeladmin, request, queryset):
    x = syncAllFromRegfox.delay()
    messages.success(request, "Sent the command to Celery. Process will be completed in Background and will update the Last Updated for Active Event when Completed.")

doRegfoxSync.short_description = "Perform a full Regfox Sync"

def doRegfoxStaffSync(modeladmin, request, queryset):
    x = syncStaffFromRegfox.delay()
    messages.success(request, "Sent the command to Celery. Process will be completed in Background and will update the Last Updated for Active Event when Completed.")

doRegfoxSync.short_description = "Perform a full Regfox Staff Sync"


@admin.decorators.action(description="Manual Update Staff Reg")
def manualUpdateStaffReg(modeladmin, request, queryset):
    for x in queryset:
        if(x.formName == "Furrydelphia 2023 Staff"):
            x.conIsStaff = True
            x.save()

@admin.decorators.action(description="Generate Badge Record")
def generateBadgeRecord(modeladmin, request, queryset):
    for x in queryset:
        badge = x.getBadge()
    messages.success(request, "Created Badge Records.")


def sendBadgeToPrint(modeladmin, request, queryset):
    for x in queryset:
        current_app.send_task("printmaster.print", [x.rId])
    messages.success(request,
                     "Sent the command to Celery. If printers are connected, they will print the badges shortly.")

sendBadgeToPrint.short_description = "Send Badge to Print Queue"

def sendToChopscreen(modeladmin, request, queryset, from_queue='r-frontreg'):

    mapping = {
        "yourLegalName.first":
            {
                "name": "intermediate.id1"
            },
        "yourLegalName.last":
            {
                "name": "intermediate.id2"
            },
        "registrationOptions":
            {
                "name": "intermediate.registrationOption"
            },
        "badgeName":
            {
                "name": "Badge Name",
                "extraAttr": False
            },
        "products.mealPlan":
            {
                "name": "Meal Plan Voucher",
                "extraAttr": False
            },
        "conTshirtSize":
            {
                "name": "Con T-Shirt Size",
                "extraAttr": False
            },
        "multipleChoice":
            {
                "name": "Jersey Size",
                "extraAttr": False
            },
        "attendeeAdditionalMerchendise.product1":
            {
              "name": "Furrydelphia 2022 Lanyard",
              "extraAttr": False
            },
        "attendeeAdditionalMerchendise.product2":
            {
                "name": "Con T-Shirt"
            },
        "attendeeAdditionalMerchendise.product3":
            {
                "name": "Ripstop Backpack"
            },
        "attendeeAdditionalMerchendise.shotGlass":
            {
              "name": "Coffee Mug"
            },
        "supersponsorAdditionalMerchendise.product1":
            {
                "name": "Crystal Shot Glass"
            },
        "supersponsorAdditionalMerchendise.product2":
            {
                "name": "Water Bottle"
            },
        "supersponsorAdditionalMerchendise.product3":
            {
                "name": "Wireless Charger"
            },
        "elitesponsorAdditionalMerchandise.product1":
            {
                "name": "Backpack"
            },
        "elitesponsorAdditionalMerchandise.product2":
            {
                "name": "Rolling Duffel Bag"
            },
        "elitesponsorAdditionalMerchandise.product3":
            {
                "name": "Crystal Rocks Glass"
            },
        "elitesponsorAdditionalMerchandise.tumbler":
            {
                "name": "Tank Top"
            },
        "customShirts.pulloverJersey":
            {
                "name": "**CUSTOM** Pullover Jersey"
            },
        "customShirts.buttonUpJersey":
            {
                "name": "**CUSTOM** Button Up Jersey"
            }
    }

    for x in queryset:
        screenData = {
            "app": "registration",
            "id": "",
            "pk": "",
            "pickList": [],
            "toLocation": "Reg Hold",
            "timeCreated": "",
            "clear": False
        }
        id1 = ""
        id2 = ""
        regOption = ""
        for y in x.fieldData:
            propLabel = ""
            try:
                propLabel = mapping[y['path']]['name']
                passover = False
                if (propLabel == "intermediate.id1"):
                    id1 = y['value']
                    passover = True
                if (propLabel == "intermediate.id2"):
                    id2 = y['value']
                    passover = True
                if (propLabel == "intermediate.registrationOption"):
                    regOption = y['value']
                    passover = True
                if(passover == False):
                    # do things
                    screenData['pickList'].append({
                        "name": propLabel,
                        "description": y['value']
                    })
            except:
                print("No Mapping for %s found" % (y['path']))

        event = Event.objects.filter(pk=cur_event_pk).first()
        regOptionResolved = ConBadgeLevelMap.objects.filter(event=event, regfoxValue=regOption).first()

        screenData['id'] = "#%s - %s %s (%s)" % (x.getBadge().number, id1, id2, regOptionResolved.badgeLevel)
        screenData['badgeNumber'] = "%s" % (x.getBadge().number)
        p = PrintJob.objects.create(
            screenData=screenData
        )
        p.screenData['timeCreate'] = p.timeCreated.isoformat()
        p.screenData['pk'] = p.pk
        p.screenData['uflsId'] = x.pk
        p.screenData['pickList'].insert(0, {"name": "Reg Level", "description": regOptionResolved.badgeLevel})
        p.screenData['pickList'].insert(0, {"name": "Attendee Name", "description": "%s %s" % (id1, id2)})

        sendToBackend = True
        if(len(p.screenData['pickList']) <= 2 and regOptionResolved.badgeHasMerch == False):
            sendToBackend = False

        Celery.send_task('receiptmanager.printRegTickets', kwargs={'attendee_info': p.screenData, 'from_queue': from_queue, 'send_to_backend': sendToBackend})

        p.save()
    messages.success(request, "Created new Print Jobs.")


def sendToChopscreenTwo(modeladmin, request, queryset, from_queue='r-frontreg-npass'):

    mapping = {
        "yourLegalName.first":
            {
                "name": "intermediate.id1"
            },
        "yourLegalName.last":
            {
                "name": "intermediate.id2"
            },
        "registrationOptions":
            {
                "name": "intermediate.registrationOption"
            },
        "badgeName":
            {
                "name": "Badge Name",
                "extraAttr": False
            },
        "products.mealPlan":
            {
                "name": "Meal Plan Voucher",
                "extraAttr": False
            },
        "conTshirtSize":
            {
                "name": "Con T-Shirt Size",
                "extraAttr": False
            },
        "multipleChoice":
            {
                "name": "Jersey Size",
                "extraAttr": False
            },
        "attendeeAdditionalMerchendise.product1":
            {
              "name": "Furrydelphia 2022 Lanyard",
              "extraAttr": False
            },
        "attendeeAdditionalMerchendise.product2":
            {
                "name": "Con T-Shirt"
            },
        "attendeeAdditionalMerchendise.product3":
            {
                "name": "Ripstop Backpack"
            },
        "attendeeAdditionalMerchendise.shotGlass":
            {
              "name": "Coffee Mug"
            },
        "supersponsorAdditionalMerchendise.product1":
            {
                "name": "Crystal Shot Glass"
            },
        "supersponsorAdditionalMerchendise.product2":
            {
                "name": "Water Bottle"
            },
        "supersponsorAdditionalMerchendise.product3":
            {
                "name": "Wireless Charger"
            },
        "elitesponsorAdditionalMerchandise.product1":
            {
                "name": "Backpack"
            },
        "elitesponsorAdditionalMerchandise.product2":
            {
                "name": "Rolling Duffel Bag"
            },
        "elitesponsorAdditionalMerchandise.product3":
            {
                "name": "Crystal Rocks Glass"
            },
        "elitesponsorAdditionalMerchandise.tumbler":
            {
                "name": "Tank Top"
            },
        "customShirts.pulloverJersey":
            {
                "name": "**CUSTOM** Pullover Jersey"
            },
        "customShirts.buttonUpJersey":
            {
                "name": "**CUSTOM** Button Up Jersey"
            }
    }

    for y in queryset:
        x = y.registrant
        screenData = {
            "app": "registration",
            "id": "",
            "pk": "",
            "pickList": [],
            "toLocation": "Reg Hold",
            "timeCreated": "",
            "clear": False
        }
        id1 = ""
        id2 = ""
        regOption = ""
        for y in x.fieldData:
            propLabel = ""
            try:
                propLabel = mapping[y['path']]['name']
                passover = False
                if (propLabel == "intermediate.id1"):
                    id1 = y['value']
                    passover = True
                if (propLabel == "intermediate.id2"):
                    id2 = y['value']
                    passover = True
                if (propLabel == "intermediate.registrationOption"):
                    regOption = y['value']
                    passover = True
                if(passover == False):
                    # do things
                    screenData['pickList'].append({
                        "name": propLabel,
                        "description": y['value']
                    })
            except:
                print("No Mapping for %s found" % (y['path']))

        event = Event.objects.filter(pk=cur_event_pk).first()
        regOptionResolved = ConBadgeLevelMap.objects.filter(event=event, regfoxValue=regOption).first()

        screenData['id'] = "#%s - %s %s (%s)" % (x.getBadge().number, id1, id2, regOptionResolved.badgeLevel)
        screenData['badgeNumber'] = "%s" % (x.getBadge().number)
        p = PrintJob.objects.create(
            screenData=screenData
        )
        p.screenData['timeCreate'] = p.timeCreated.isoformat()
        p.screenData['pk'] = p.pk
        p.screenData['uflsId'] = x.pk
        p.screenData['pickList'].insert(0, {"name": "Reg Level", "description": regOptionResolved.badgeLevel})
        p.screenData['pickList'].insert(0, {"name": "Attendee Name", "description": "%s %s" % (id1, id2)})

        Celery.send_task('receiptmanager.printRegTickets', kwargs={'attendee_info': p.screenData, 'from_queue': from_queue})

        p.save()
    messages.success(request, "Created new Print Jobs.")

sendToChopscreenTwo.short_description = "Create Print Jobs for ChopScreen"
sendToChopscreen.short_description = "Create Print Jobs for ChopScreen"

def updateConData(modeladmin, request, queryset):
    for x in queryset:
        for y in x.fieldData:
            if (y['path'] == "yourLegalName.first"):
                x.conFirstName = y['value']
            if (y['path'] == "yourLegalName.last"):
                x.conLastName = y['value']
            if (y['path'] == "email"):
                x.conEmail = y['value'].lower()
            if (y['path'] == "badgeName"):
                x.conBadgeName = y['value']
            if (y['path'] == "dateOfBirth"):
                x.conDOB = y['value']
            if (y['path'] == "registrationOptions"):
                x.conRegLevel = ConBadgeLevelMap.objects.filter(event=Event.objects.filter(pk=cur_event_pk).first(), regfoxValue=y['value']).first()
            x.save()
    messages.success(request, "Updated all Con Information in Top Level.")

updateConData.short_description = "Update Con Info from Regfox Data"

def createEmailReservationLinks(modeladmin, request, queryset):
    for x in queryset:
        n = ReservationKey.objects.filter(email=x.conEmail.lower().replace(" ",""))
        if n.count() == 0:
            ReservationKey.objects.create(
                email=x.conEmail.lower().replace(" ",""),
                group="Attendee Sponsors",
                reservation={}
            )
    messages.success(request, "All done.")

createEmailReservationLinks.short_description = "Create e-mail registration link keys"

def runConnectedAttachSync(modeladmin, request, queryset):
    for x in queryset:
        x.updateAttachedRegistrant()
    messages.success(request, "All done.")

runConnectedAttachSync.short_description = "Sync Registrant Data for WX Action"

class RegistrantDataAdmin(ImportExportModelAdmin):
    list_display = ['conFirstName', 'conLastName', 'conDOB', 'determineAge', 'conCheckedIn', 'conCheckedInDate', 'conEmail', 'conBadgeName', 'conRegLevel', 'event']
    list_filter = ('conIsStaff', 'conIsDealer', 'conIsDealerAssistant', 'conCheckedIn', 'hasMealPlan', 'conRegLevel', 'event')
    actions = [doRegfoxSync, sendBadgeToPrint, sendToChopscreen, updateConData, generateBadgeRecord, createEmailReservationLinks, doRegfoxStaffSync, manualUpdateStaffReg]

class BadgeAdmin(ImportExportModelAdmin):
    search_fields = ['number']
    list_display = ['number', 'registrant']
    actions = [sendToChopscreenTwo]

class WebconnexActionAdmin(ImportExportModelAdmin):
    actions = [runConnectedAttachSync]

admin.site.register(Event)
admin.site.register(RegistrantData, RegistrantDataAdmin)
admin.site.register(ConBadgeLevelMap)
admin.site.register(PrintJob)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(WebconnexAction, WebconnexActionAdmin)