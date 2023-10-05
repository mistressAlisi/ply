from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from registrar.forms import RegistrantForm,ConditionsForm
from registration.models import ConBadgeLevelMap, Event, RegistrantData
from registrar.models import Registrant, RegistrantLevel
from django.conf import settings
from decouple import config
from decimal import *
import datetime,uuid,stripe,json

cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="")

stripe.api_key =  settings.PAYMENT_STRIPE_SECRET_KEY
# Create your views here.
def regForm1(request):
    regform = RegistrantForm()
    condform = ConditionsForm()
    sessionRegs = []
    sessionTotal = Decimal(0)
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    context = {'regform':regform,'condform':condform,'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal}
    return render(request,"registrar/form1.html",context)

def createReg1(request):
    # Check for Terms and conditions:
    if ('agreeCOC' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the Code of Conduct to register."},safe=False)
    if ('agreeRFP' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the Refund Policy to register."},safe=False)
    if ('agreeCVD' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the COVID Policy to register."},safe=False)
    # now validate the data:
    registrant = RegistrantForm(request.POST)

    if (not registrant.is_valid()):
        return JsonResponse({"res":"err","e":registrant.errors.as_json()},safe=False)
    # Save the registrant:
    regdata = registrant.save()
    regdata.agreeCOC = True
    regdata.agreeCOCDate = datetime.datetime.now()
    regdata.agreeRFP = True
    regdata.agreeRFPDate = datetime.datetime.now()
    regdata.agreeCVD = True
    regdata.agreeCVDDate = datetime.datetime.now()

    # add the registrant to the session:
    if 'regs' not in request.session:
        request.session['regs'] = []
    request.session['regs'].append(str(regdata.uuid))
    request.session.modified = True
    # Update regdata with totals and save:
    total = regdata.fdDonation + regdata.chDonation + regdata.level.cost
    regdata.total = total
    regdata.outstandingAmount = total
    regdata.amount  = 0
    regdata.save()
    return JsonResponse({"res":"ok"},safe=False)


def cartContents(request):
    if 'regs' not in request.session:
            return JsonResponse({"res":"ok","d":[]},safe=False)
    resdata = []
    print(request.session['regs'])
    for d in request.session['regs']:
        regobj = Registrant.objects.get(pk=d)
        resdata.append({'n':regobj.firstName+' '+regobj.lastName,'l':regobj.level.label,'t':regobj.total})
    return JsonResponse({"res":"ok","resdata":resdata},safe=False)

def cartContentsHTML(request):
    sessionTotal = 0
    sessionRegs = []
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal}
    return render(request,"registrar/render_cart_contents.html",context)

def removeFromCart(request,itm):
    if itm in request.session['regs']:
        request.session['regs'].remove(itm)
        request.session.modified = True
    return JsonResponse({"res":"ok"},safe=False)


def checkout(request):
    sessionRegs = []
    sessionTotal = 0
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal}
    return render(request,"registrar/checkout.html",context)

def checkoutExec(request):
    domain = settings.PAYMENT_HOST
    if ('regs' not in request.session):
        return redirect("/app/registrar/")
    line_items = []
    metadata = {'action':'activate','regs':",".join(request.session['regs'])}
    for d in request.session['regs']:
        regobj = Registrant.objects.get(pk=d)
        if (settings.PAYMENT_STRIPE_TEST == True):
            line_items.append({'price':regobj.level.stripe_price_test,'quantity':1})
        else:
            line_items.append({'price':regobj.level.stripe_price,'quantity':1})
        # if they set up donations...
        if ((regobj.fdDonation > 0) or (regobj.chDonation >0)):
            totalDonation = int(regobj.fdDonation + regobj.chDonation)
            line_items.append({'price':settings.PAYMENT_STRIPE_DONATION_ITEM,'quantity':totalDonation})
    #print(line_items)
    #print(metadata)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        metadata = metadata,
        line_items = line_items,
        mode='payment',
        success_url=domain + 'app/registrar/success',
        cancel_url=domain + 'app/registrar/checkout',
    )
    return redirect(checkout_session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.PAYMENT_STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
        regEvent = Event.objects.get(pk=cur_event_pk)
        # Activate regs!
        if 'metadata' in event['data']['object']:
            if (event['data']['object']['metadata']['action'] == 'activate'):
                regs = event['data']['object']['metadata']["regs"].split(",")
                for r in regs:
                    regobj = Registrant.objects.get(pk=r)
                    regobj.paidDate = datetime.datetime.now()
                    regobj.paid = True
                    regobj.outstandingAmount = 0
                    regobj.save()

                    formDataFormatting = [
                        {"path": "yourLegalName.first", "label": "First Name", "value": regobj.firstName},
                        {"path": "yourLegalName.last", "label": "Last Name", "value": regobj.lastName},
                        {"path": "preferredName", "label": "Preferred Name", "value": regobj.firstName},
                        {"path": "email", "label": "Email", "value": regobj.email},
                        {"path": "phoneNumber", "label": "Phone Number", "value": regobj.phone},
                        {"path": "address.city", "label": "City", "value": regobj.city},
                        {"path": "address.country", "label": "Country", "value": regobj.country},
                        {"path": "address.postalCode", "label": "ZIP/Postal Code", "value": regobj.zip},
                        {"path": "address.state", "label": "State", "value": regobj.addr2},
                        {"path": "address.street1", "label": "Street Address", "value": regobj.addr1},
                        {"path": "address.street2", "label": "Street Address", "value": regobj.addr2},
                        {"path": "badgeName", "label": "Badge Name", "value": regobj.badgeName},
                    ]

                    registration = RegistrantData(
                        event=regEvent,
                        rUUID=regobj.uuid,
                        displayId=str(regobj.uuid),
                        formId='UFLSReg-v1.0',
                        formName='UFLS Registrar',
                        formAccRef='Stripe',
                        orderCustomerId=regobj.email,
                        customerId=regobj.email,
                        orderId=str(regobj.uuid),
                        orderDisplayId=str(regobj.uuid),
                        orderNumber=str(regobj.uuid),
                        orderEmail=regobj.email,
                        status='completed',
                        total=regobj.total,
                        amount=regobj.total,
                        outstandingAmount=0,
                        currency='USD',
                        fieldData=formDataFormatting,
                        metadata=regobj.level.label,
                        checkedIn=False,
                        dateCreated=datetime.datetime.now(),
                        conFirstName=regobj.firstName,
                        conLastName=regobj.lastName,
                        conEmail=regobj.email,
                        conBadgeName=regobj.badgeName,
                        conDOB=regobj.dob.strftime("%Y-%m-%d"),
                        conRegLevel=ConBadgeLevelMap.objects.filter(stripePrice=regobj.level.stripe_price).first()
                    )
                    registration.save()

    return HttpResponse(status=200)




def success(request):
    sessionRegs = []
    sessionTotal = 0
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    request.session['regs'] = []
    request.session.modified = True
    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal}
    return render(request,"registrar/success.html",context)

