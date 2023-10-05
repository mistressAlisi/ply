from subprocess import check_output

from celery import shared_task
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from .models import ConBadgeLevelMap, Event, RegistrantData
import urllib3, os, json
from django.utils import timezone
from django.core.mail import send_mail
from decouple import config


cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="")

@shared_task
def sendHotelLinkRemindersToEmails(lst):
    # list format:
    # [(email1, link1), (email2, link2)]
    for x in lst:
        msg = """
        Hello,<br>
        <br>
        You are receiving this message because your Registration for Furrydelphia this year has granted you early access to our room block! As part of your benefits, below is a link to the online pre-reservation system for our Hotel. You can use this system to pre-reserve a hotel room before General Availability.<br>
        <br>
        <br>
        <p>Here are some important notes about this link:</p>
        <ol>
            <li><strong>This link will be valid until April 28th, 2023.</strong></li>
            <li>Do not share this link, it is for you and you alone.</li>
            <li>Once you use this link to submit a pre-reservation, it will become invalid and cannot be shared.</li>
            <li>You can only use this system to pre-reserve one room. If you want to book more rooms, reach out to us at bookings@furrydelphia.org or wait until General Availability.</li>
        </ol>
        <p>If you have any more questions, please check out the FAQ at <a href="https://reservations.furrydelphia.org/">https://reservations.furrydelphia.org/</a>
        <hr>
            <p>Booking Link: <a href="%s">%s</a>
        <hr>
        Thanks,<br>
        The Furrydelphia Hotel Team<br>
        <hr>
        <p>Questions? DO NOT REPLY TO THIS E-MAIL. This e-mail account is unmonitored. Please e-mail bookings@furrydelphia.org</p>
        """ % (x[1], x[1])
        send_mail(
            subject="Furrydelphia 2023 - Hotel Pre-reservation Link for Super and Elite Sponsors",
            html_message=msg,
            message="Please allow HTML Messages to Continue.",
            from_email="Furrydelphia <bots@furrydelphia.org>",
            recipient_list=[x[0]]
        )

@shared_task
def sendHotelLinksToEmails(lst):
    # list format:
    # [(email1, link1), (email2, link2)]
    for x in lst:
        msg = """
        Hello,<br>
        <br>
        You are receiving this message because your Registration for Furrydelphia this year has granted you early access to our room block and have not used your link yet to pre-reserve a hotel room! As part of your benefits, below is a link to the online pre-reservation system for our Hotel. You can use this system to pre-reserve a hotel room before General Availability.<br>
        <br>
        <br>
        <p>Here are some important notes about this link:</p>
        <ol>
            <li><strong>This link will be valid until April 28th, 2023.</strong></li>
            <li>Do not share this link, it is for you and you alone.</li>
            <li>Once you use this link to submit a pre-reservation, it will become invalid and cannot be shared.</li>
            <li>You can only use this system to pre-reserve one room. If you want to book more rooms, reach out to us at bookings@furrydelphia.org or wait until General Availability.</li>
        </ol>
        <p>If you have any more questions, please check out the FAQ at <a href="https://reservations.furrydelphia.org/">https://reservations.furrydelphia.org/</a>
        <hr>
            <p>Booking Link: <a href="%s">%s</a>
        <hr>
        Thanks,<br>
        The Furrydelphia Hotel Team<br>
        <hr>
        <p>Questions? DO NOT REPLY TO THIS E-MAIL. This e-mail account is unmonitored. Please e-mail bookings@furrydelphia.org</p>
        """ % (x[1], x[1])
        send_mail(
            subject="Furrydelphia 2023 - REMINDER - Hotel Pre-reservation Link for Super and Elite Sponsors",
            html_message=msg,
            message="Please allow HTML Messages to Continue.",
            from_email="Furrydelphia <bots@furrydelphia.org>",
            recipient_list=[x[0]]
        )

@shared_task
def syncAllFromRegfox2021():
    event = Event.objects.filter(pk=cur_event_pk).first()
    apikey = config("UFLS_REGFOX_API_KEY", default="")
    http = urllib3.PoolManager()
    hasMore = True
    startingAfter = 0
    while hasMore == True:
        r = http.request('GET', 'https://api.webconnex.com/v2/public/search/registrants?product=regfox.com&pretty=false&formId=%s&startingAfter=%s' % (event.regfoxPageCode, startingAfter), headers={"apiKey": apikey}, verify=False)
        incomingData = json.loads(r.data.decode('utf-8'))
        for x in incomingData['data']:
            if(x['status'] == "pending-CHANGEMETODO"):
                pass
                #print("Skipping Pending Transaction")
            else:
                lkp = RegistrantData.objects.filter(formId=x['formId'], rId=x['id'], displayId=x['displayId']).first()
                if(lkp == None):
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
                    #try:
                    #    lkp.dateUpdated = x['dateUpdated']
                    #except KeyError:
                    #    print("Could not update dateUpdated for %s" % lkp.pk)
                    #    pass
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2020STAFF" or y['value'] == "FD2021STAFF":
                                lkp.conIsStaff = True
                            if y['value'].find("DEALER") != -1:
                                lkp.conIsDealer = True
                            if y['value'].find("-A") != -1:
                                lkp.conIsDealerAssistant = True
                        if(y['path'] == "yourLegalName.first"):
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
                            lkp.conRegLevel = ConBadgeLevelMap.objects.filter(event=event, regfoxValue=y['value']).first()
                    lkp.save()
                    #print("New Registrant Added: " + lkp.displayId)
                else:
                    lkp.rId=x['id']
                    lkp.displayId=x['displayId']
                    lkp.formId=x['formId']
                    lkp.formName=x['formName']
                    lkp.formAccRef=x['formAccRef']
                    lkp.orderCustomerId=x['orderCustomerId']
                    lkp.customerId=x['customerId']
                    lkp.orderId=x['orderId']
                    lkp.orderDisplayId=x['orderDisplayId']
                    lkp.orderNumber=x['orderNumber']
                    lkp.orderEmail=x['orderEmail']
                    lkp.status=x['status']
                    lkp.total=x['total']
                    lkp.amount=x['amount']
                    lkp.outstandingAmount=x['outstandingAmount']
                    lkp.currency=x['currency']
                    lkp.fieldData=x['fieldData']
                    lkp.metadata=x['metadata']
                    lkp.checkedIn=x['checkedIn']
                    lkp.dateCreated=x['dateCreated']
                    #lkp.dateUpdated=x['dateUpdated']
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2020STAFF" or y['value'] == "FD2021STAFF":
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
                    lkp.save()
                    #print("Registrant Updated: " + lkp.displayId)
        try:
            #print(incomingData['hasMore'])
            #print(incomingData['startingAfter'])
            hasMore = incomingData['hasMore']
            startingAfter = incomingData['startingAfter']
            #print("About to start page beginning at: " + str(startingAfter))
        except:
            hasMore = False
            #print("Exiting loop because of a fault or because we've reached the end.")
    event.timeLastSync = timezone.now()
    event.save()

@shared_task
def renderBadgePdf(id):
    if id == 'lunch':
        c = check_output('/app/bin/wkhtmltopdf --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --background --page-width 86 --page-height 54 %s %s' % ('https://backend.furrydelphia.org/app/badge-lunch/toHtml/', '/app/staticfiles/lunch.pdf'), shell=True)
    if id == 'back':
        c = check_output('/app/bin/wkhtmltopdf --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --background --page-width 86 --page-height 54 %s %s' % ('https://backend.furrydelphia.org/app/badge-back/toHtml/', '/app/staticfiles/back.pdf'), shell=True)
    else:
        c = check_output('/app/bin/wkhtmltopdf --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --background --page-width 86 --page-height 54 %s %s' % ('https://backend.furrydelphia.org/app/badge/toHtml/%s/' % (id), '/app/staticfiles/badge_%s.pdf' % (id)), shell=True)
    return True

@shared_task
def syncStaffFromRegfox():
    event = Event.objects.filter(pk=cur_event_pk).first()
    apikey = config("UFLS_REGFOX_API_KEY", default="")
    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    hasMore = True
    startingAfter = 0
    print("Starting, hasMore = ", hasMore)
    while hasMore == True:
        r = http.request('GET',
                         'https://api.webconnex.com/v2/public/search/registrants?product=regfox.com&pretty=false&formId=%s&startingAfter=%s' % (event.regfoxStaffPageCode, startingAfter), headers={"apiKey": apikey})
        print("request: ", r.data)
        incomingData = json.loads(r.data.decode('utf-8'))
        for x in incomingData['data']:
            if(x['status'] == "pending-CHANGEMETODO"):
                pass
                #print("Skipping Pending Transaction")
            else:
                lkp = RegistrantData.objects.filter(formId=x['formId'], rId=x['id'], displayId=x['displayId'], event=event).first()
                if(lkp == None):
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
                    #try:
                    #    lkp.dateUpdated = x['dateUpdated']
                    #except KeyError:
                    #    print("Could not update dateUpdated for %s" % lkp.pk)
                    #    pass

                    # Hardcoding this isStaff flag because we're directly syncing from the staff page.
                    lkp.conIsStaff = True
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'].find("DEALER") != -1:
                                lkp.conIsDealer = True
                            if y['value'].find("-A") != -1:
                                lkp.conIsDealerAssistant = True
                        if(y['path'] == "yourLegalName.first"):
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
                            lkp.conRegLevel = ConBadgeLevelMap.objects.filter(event=event, regfoxValue=y['value']).first()
                    lkp.save()
                    #print("New Registrant Added: " + lkp.displayId)
                else:
                    lkp.rId=x['id']
                    lkp.displayId=x['displayId']
                    lkp.formId=x['formId']
                    lkp.formName=x['formName']
                    lkp.formAccRef=x['formAccRef']
                    lkp.orderCustomerId=x['orderCustomerId']
                    lkp.customerId=x['customerId']
                    lkp.orderId=x['orderId']
                    lkp.orderDisplayId=x['orderDisplayId']
                    lkp.orderNumber=x['orderNumber']
                    lkp.orderEmail=x['orderEmail']
                    lkp.status=x['status']
                    lkp.total=x['total']
                    lkp.amount=x['amount']
                    lkp.outstandingAmount=x['outstandingAmount']
                    lkp.currency=x['currency']
                    lkp.fieldData=x['fieldData']
                    lkp.metadata=x['metadata']
                    lkp.checkedIn=x['checkedIn']
                    lkp.dateCreated=x['dateCreated']
                    #lkp.dateUpdated=x['dateUpdated']
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2022STAFF":
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
                    lkp.save()
                    #print("Registrant Updated: " + lkp.displayId)
        try:
            #print(incomingData['hasMore'])
            #print(incomingData['startingAfter'])
            hasMore = incomingData['hasMore']
            startingAfter = incomingData['startingAfter']
            #print("About to start page beginning at: " + str(startingAfter))
        except:
            hasMore = False
            #print("Exiting loop because of a fault or because we've reached the end.")
    event.timeLastSync = timezone.now()
    event.save()



@shared_task
def syncAllFromRegfox():
    event = Event.objects.filter(pk=cur_event_pk).first()
    i = event.timeLastSync.isoformat().split("+")[0]
    apikey = config("UFLS_REGFOX_API_KEY", default="")
    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    hasMore = True
    startingAfter = 0
    print("Starting, hasMore = ", hasMore)
    while hasMore == True:
        r = http.request('GET',
                         'https://api.webconnex.com/v2/public/search/registrants?product=regfox.com&pretty=false&formId=%s&startingAfter=%s&dateUpdatedAfter=%s' % (event.regfoxPageCode, startingAfter, i+"Z"), headers={"apiKey": apikey})
        print("request: ", r.data)
        incomingData = json.loads(r.data.decode('utf-8'))
        for x in incomingData['data']:
            if(x['status'] == "pending-CHANGEMETODO"):
                pass
                #print("Skipping Pending Transaction")
            else:
                lkp = RegistrantData.objects.filter(formId=x['formId'], rId=x['id'], displayId=x['displayId'], event=event).first()
                if(lkp == None):
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
                    #try:
                    #    lkp.dateUpdated = x['dateUpdated']
                    #except KeyError:
                    #    print("Could not update dateUpdated for %s" % lkp.pk)
                    #    pass
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2022STAFF":
                                lkp.conIsStaff = True
                            if y['value'].find("DEALER") != -1:
                                lkp.conIsDealer = True
                            if y['value'].find("-A") != -1:
                                lkp.conIsDealerAssistant = True
                        if(y['path'] == "yourLegalName.first"):
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
                            lkp.conRegLevel = ConBadgeLevelMap.objects.filter(event=event, regfoxValue=y['value']).first()
                    lkp.save()
                    #print("New Registrant Added: " + lkp.displayId)
                else:
                    lkp.rId=x['id']
                    lkp.displayId=x['displayId']
                    lkp.formId=x['formId']
                    lkp.formName=x['formName']
                    lkp.formAccRef=x['formAccRef']
                    lkp.orderCustomerId=x['orderCustomerId']
                    lkp.customerId=x['customerId']
                    lkp.orderId=x['orderId']
                    lkp.orderDisplayId=x['orderDisplayId']
                    lkp.orderNumber=x['orderNumber']
                    lkp.orderEmail=x['orderEmail']
                    lkp.status=x['status']
                    lkp.total=x['total']
                    lkp.amount=x['amount']
                    lkp.outstandingAmount=x['outstandingAmount']
                    lkp.currency=x['currency']
                    lkp.fieldData=x['fieldData']
                    lkp.metadata=x['metadata']
                    lkp.checkedIn=x['checkedIn']
                    lkp.dateCreated=x['dateCreated']
                    #lkp.dateUpdated=x['dateUpdated']
                    for y in x['fieldData']:
                        if (y['path'] == "couponCode"):
                            if y['value'] == "FD2022STAFF":
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
                    lkp.save()
                    #print("Registrant Updated: " + lkp.displayId)
        try:
            #print(incomingData['hasMore'])
            #print(incomingData['startingAfter'])
            hasMore = incomingData['hasMore']
            startingAfter = incomingData['startingAfter']
            #print("About to start page beginning at: " + str(startingAfter))
        except:
            hasMore = False
            #print("Exiting loop because of a fault or because we've reached the end.")
    event.timeLastSync = timezone.now()
    event.save()