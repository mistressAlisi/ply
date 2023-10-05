import base64
import hashlib
import hmac
import json
import os
import random
from base64 import decodebytes
from time import sleep

import requests
import tablib
import urllib3
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions

from .models import RegistrantData, WebconnexAction, Event, ConBadgeLevelMap, Badge
from django.http import JsonResponse, HttpResponse, FileResponse, Http404, StreamingHttpResponse
from subprocess import check_output
from .admin import sendToChopscreen
from ufls.celery import app as Celery
from .tasks import syncAllFromRegfox, renderBadgePdf
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser
from escpos.printer import Network
from ufls.printerhelpers.poshelpers import center42,receiptHeader,receiptLineItem,receiptSignatureLine
from PIL import Image, ImageDraw, ImageFont
from urllib3 import PoolManager
from io import BytesIO, StringIO
from decouple import config,Csv

# Create your views here.

def renderLabel(request, id):
    registrant = get_object_or_404(RegistrantData, pk=id)
    badge = registrant.getBadge()
    return render(request, 'labeler.html', context={"badge": badge})

def labelerpdf(request, id):
    c = check_output(
        'wkhtmltopdf --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --background --page-width 50 --page-height 11.5 %s %s' % (
        'https://backend.furrydelphia.org/app/label/print/%s/' % (id), '/app/staticfiles/printlabel-%s.pdf' % (id)), shell=True)

    f = open('/app/staticfiles/printlabel-%s.pdf' % (id), 'rb')
    pdf_contents = f.read()
    f.close()

    return HttpResponse(pdf_contents, content_type='application/pdf')

def displayBadgeHtml(request, id):
    registrant = get_object_or_404(RegistrantData, pk=id)
    if(registrant.displayImageUrl() != "Error"):
        i = "whatever"
    else:
        i = "stock"
    badge = registrant.getBadge()
    return render(request, 'printing.html', context={"badge": badge, "image": i})


def badgeToPdf(request, id):
    x = Celery.send_task('badgerenderer.renderBadgePdf', kwargs={"id": id})

    try:
        return HttpResponse('OK')
    except FileNotFoundError:
        raise Http404()

def badgeBackToHtml(request):
    return render(request, 'printing_back.html')

def badgeBackToPdf(request):
    x = Celery.send_task('badgerenderer.renderBadgePdf', kwargs={"id": 'back'})
    #c = check_output('wkhtmltopdf --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --background --page-width 86 --page-height 54 %s %s' % ('https://backend.furrydelphia.org/app/badge-back/toHtml/', '/app/staticfiles/back.pdf'), shell=True)
    #print(c)
    try:
        return HttpResponse('OK')
    except FileNotFoundError:
        raise Http404()

@permission_classes([IsAdminUser])
@api_view(['GET'])
def lunchPassToHtml(request):
    return render(request, 'printing_lunch.html')

def lunchPassToPdf(request):
    x = Celery.send_task('badgerenderer.renderBadgePdf', kwargs={"id": 'lunch'})
    try:
        return HttpResponse('OK')
    except FileNotFoundError:
        raise Http404()

@permission_classes([IsAdminUser])
@api_view(['GET'])
def testReceiptPrinter(request):
    testprinter = Network("10.243.29.248",profile="TM-T88IV")

    image = Image.new("RGB", (300, 125), "white")
    draw = ImageDraw.Draw(image)
    badge_number = "324"
    spacing = {
        "3": 55,
        "4": 0
    }
    print(len(badge_number))
    draw.text((spacing[str(len(badge_number))],0), badge_number, (0,0,0), ImageFont.truetype("staticfiles/Courier.ttf", 100))
    image.save("text.png")


    print(testprinter.profile.features)
    #testprinter.image("staticfiles/fdlogo.png", center=True)
    testprinter.image("text.png", center=True)
    testprinter.textln(center42("Furrydelphia 2022 Registration"))
    testprinter.ln(count=1)
    testprinter.textln(center42("Registration Time: 2022-07-14 13:55:55"))
    testprinter.ln(count=1)
    testprinter.textln(receiptHeader())
    testprinter.textln(receiptLineItem("Attendee Badge #234", "1"))
    testprinter.textln(receiptLineItem("   Badge Name: Yuuk does a thing!", ""))
    testprinter.textln(receiptLineItem("   Printer: Color Attendee", ""))
    testprinter.textln(receiptLineItem("Con Book", "1"))
    testprinter.textln(receiptLineItem("Con T-shirt", "1"))
    testprinter.textln(receiptLineItem("   Size: XXL", ""))
    testprinter.ln(count=1)
    testprinter.textln(receiptSignatureLine())
    #testprinter.qr(content="Test", center=True)
    testprinter.cut()
    return JsonResponse({"status": 200})

@permission_classes([IsAdminUser])
def issueRegfoxSync(request):
    syncAllFromRegfox.delay()
    return JsonResponse({"status": "success", "message": "Sent command to Celery for Regfox Processing. Command takes about 1-2 minutes."})


def printBadgeBack(request):

    Celery.send_task(name='printmaster.print', kwargs={"id": "back", "queue": "blackonly"})

    return JsonResponse({"sent": True})

@permission_classes([IsAdminUser])
def printLunchPass(request):

    Celery.send_task(name='printmaster.print', kwargs={"id": "lunch", "queue": "blackonly"})

    return JsonResponse({"sent": True})

# yes yes yes i know this is unsafe, i dont know how to fix it. its a webhook handle.
@csrf_exempt
@permission_classes([IsAdminUser])
def printBadge(request, id, from_queue='r-frontreg'):

    registrant = get_object_or_404(RegistrantData, pk=id)
    badge = registrant.getBadge()
    t = from_queue
    from_queue = request.GET.get("fromQueue") or t
    #params = {
    #    "x1": int(request.GET["x1"]) or 0,
    #    "x2": int(request.GET["x2"]) or 0,
    #    "y1": int(request.GET["y1"]) or 0,
    #    "y2": int(request.GET["y2"]) or 0,
    #}

    body = json.loads(request.body)
    #if(body['b64'] != None):
    #    img = Image.open(BytesIO(base64.b64decode(body['b64'].split(":image/png;base64,")[1])))
    #    img_str = BytesIO()
    #    img.save(img_str, format="PNG")
    #    imuf = InMemoryUploadedFile(img_str, None, 'bamf-%s.png' % (random.randrange(1,10000)), 'image/png',
    #                         img_str.tell(), None)
    #    registrant.croppedImage = imuf
    registrant.conCheckedIn = True
    registrant.conCheckedInDate = timezone.localtime(timezone.now())
    registrant.save()
    sendToChopscreen(None, request, [registrant], from_queue)

    """
    "mainqueue": ["DC1", "DC2", "DC3"],
        "minor15queue": ["DC4"],
        "minor14queue": ["DC5"],
        "daypassqueue": ["DC6"],
        "dealersdenqueue": ["DC7"]
    """

    # queue = ""
    # if(registrant.determineAge() == 18):
    #     queue = "mainqueue"
    # if(registrant.conRegLevel.badgeLevel == "Friday Day Pass" or registrant.conRegLevel.badgeLevel == "Saturday Day Pass" or registrant.conRegLevel.badgeLevel == "Sunday Day Pass"):
    #     queue = "daypassqueue"
    # if(registrant.determineAge() == 15):
    #     queue = "minor15queue"
    # if(registrant.determineAge() == 14):
    #     queue = "minor14queue"
    # if(registrant.conIsDealer or registrant.conIsDealerAssistant):
    #     queue = "dealersdenqueue"

    # celery
    #x = Celery.send_task('badgerenderer.renderBadgePdf', kwargs={"id": registrant.pk})
    #sleep(3)
    #Celery.send_task(name='printmaster.print', kwargs={"id": registrant.pk, "queue": queue})

    return JsonResponse({"registrant": registrant.pk, "badge_number": badge.number})

# yes yes yes i know this is unsafe, i dont know how to fix it. its a webhook handle.
@csrf_exempt
def handleRegfoxWebhook(request):
    sig = request.headers.get("X-Webconnex-Signature") or ""

    signature = hmac.new(
        bytearray(config("UFLS_REGFOX_WEBHOOK_HMAC", default="no"), 'utf-8'),
        request.body,
        hashlib.sha256
    ).hexdigest()

    if sig == signature:
        w = WebconnexAction.objects.create(
            raw_data=json.loads(request.body),
            _type=json.loads(request.body)['eventType']
        )
        w.updateAttachedRegistrant()
        w.acted_upon = True
        w.save()

        return JsonResponse({"status": "Created"})
    else:
        return Http404()


def uploadCustomArtwork(request, id):
    body = json.loads(request.body)
    registrant = get_object_or_404(RegistrantData, pk=id)
    if (body['b64'] != None):
        img = Image.open(BytesIO(base64.b64decode(body['b64'].split(":image/png;base64,")[1])))
        img_str = BytesIO()
        img.save(img_str, format="PNG")
        imuf = InMemoryUploadedFile(img_str, None, 'bamf-%s.png' % (random.randrange(1, 10000)), 'image/png',
                                    img_str.tell(), None)
        registrant.customUploadPicture = imuf
        registrant.isCustomPicture = True
    registrant.save()
    return JsonResponse({"status": "OK"})

import requests
# have this function in file where you keep your util functions
def url2yield(url, chunksize=1024):
   s = requests.Session()
   # Note: here i enabled the streaming
   response = s.get(url, stream=True)

   chunk = True
   while chunk :
      chunk = response.raw.read(chunksize)

      if not chunk:
         break

      yield chunk

def sneakyDeets(request, id):
    r = get_object_or_404(RegistrantData, pk=id)
    if (r.displayImageUrl() != 'https://backend.furrydelphia.org/static/generic.jpeg' and r.displayImageUrl() != None and r.displayImageUrl() != "Error"):
        return StreamingHttpResponse(url2yield(r.displayImageUrl()), content_type="image/jpeg")
    return JsonResponse({"uhh...": "this isn't for you deborah"})


@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def exportBadges(request):
    badges = Badge.objects.filter(event=Event.objects.get(pk=os.getenv("CURRENT_EVENT_PK")), registrant__status="completed")
    data = tablib.Dataset()
    data.headers = ("FirstName","LastName","BadgeName","Number","Level")
    for x in badges:
        data.append([
            x.registrant.conFirstName,
            x.registrant.conLastName,
            x.registrant.conBadgeName,
            "2023-%s" % x.number,
            x.registrant.determineBadgeLevel()
        ])


    response = HttpResponse(data.export('xlsx'), content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % ("export-badges")
    return response

@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def exportRegistrants(request):
    badges = RegistrantData.objects.filter(event=Event.objects.get(pk=os.getenv("CURRENT_EVENT_PK")), status="completed")
    data = tablib.Dataset()
    data.headers = ("email","name")
    for x in badges:
        data.append([
            x.conEmail,
            "%s %s" % (x.conFirstName, x.conLastName),
        ])


    response = HttpResponse(data.export('xlsx'), content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % ("export-registrants")
    return response
