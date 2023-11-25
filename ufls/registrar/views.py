from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from ufls.registrar.forms import RegistrantForm,ConditionsForm
from ufls.event.models import Event,EventCommunityMapping
from ufls.registrar.models import Registrant, RegistrantLevel, RegistrantData, \
     RegistrarLevelLootView, RegistrationLoot, RegistrantLootFulfillment, RegistrationLevelLoot
from django.conf import settings
from decouple import config
from decimal import *
import datetime,uuid,stripe,json
from ply.toolkit import vhosts
from ply.toolkit import logger as plylog
log = plylog.getLogger('ufls.registrar.views',name='ufls.registrar.views')
cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="")

stripe.api_key =  settings.PAYMENT_STRIPE_SECRET_KEY
# Create your views here.
def regForm1(request):
    vhost,community = vhosts.get_vhost_and_community(request)
    if request.user.is_authenticated:
        regform = RegistrantForm(user=request.user,community=community)
    else:
        regform = RegistrantForm()
    condform = ConditionsForm()
    sessionRegs = []
    sessionTotal = Decimal(0)
    sessionLoot = []
    lootTotal = Decimal(0)
    if 'loot_cart' in request.session:
        for k in request.session['loot_cart']:
            item = RegistrationLoot.objects.get(pk=k)
            subtotal = int(request.session['loot_cart'][k])*item.cost
            sessionLoot.append({'item':item,'id':k,'count':request.session['loot_cart'][k],'subtotal':subtotal})
            lootTotal += Decimal(subtotal)

    event_data = EventCommunityMapping.objects.get(community=community)
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    context = {'regform':regform,'condform':condform,'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal,'event':event_data.event,'community':community,'active_1':True,'sessionLoot':sessionLoot,'lootTotal':lootTotal,'is_logged_in':request.user.is_authenticated}
    return render(request,"registrar/form1.html",context)


def createReg1(request):
    vhost,community = vhosts.get_vhost_and_community(request)
    event_data = EventCommunityMapping.objects.get(community=community)
    # Check for Terms and conditions:
    if ('agreeCOC' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the Code of Conduct to register."},safe=False)
    if ('agreeRFP' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the Refund Policy to register."},safe=False)
    if ('agreeCVD' not in request.POST):
        return JsonResponse({"res":"err","e":"You must agree to the COVID Policy to register."},safe=False)
    # now validate the data:
    if request.user.is_authenticated:
        registrant = RegistrantForm(request.POST,user=request.user,community=community)
    else:
        registrant = RegistrantForm(request.POST)
    if (not registrant.is_valid()):
        return JsonResponse({"res":"err","e":registrant.errors.as_json()},safe=False)
    # Save the registrant:
    regdata = registrant.save()
    regdata.event = event_data.event
    regdata.agreeCOC = True
    regdata.agreeCOCDate = datetime.datetime.now()
    regdata.agreeRFP = True
    regdata.agreeRFPDate = datetime.datetime.now()
    regdata.agreeCVD = True
    regdata.agreeCVDDate = datetime.datetime.now()
    regdata.save()
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

def createRegLoot(request):
    pkeys = request.POST.keys()
    #if 'loot_cart' not in request.session:
    request.session["loot_cart"] = {}
    for k in request.POST:
        if k.startswith("loot_"):
            request.session["loot_cart"][k[5:]] = request.POST[k]*1
    request.session.modified = True
    return JsonResponse({"res":"ok"},safe=False)

def cartContents(request):
    if 'regs' not in request.session:
            return JsonResponse({"res":"ok","d":[]},safe=False)
    resdata = []
    sessionLoot = []
    if 'loot_cart' in request.session:
        for k in request.session['loot_cart']:
            item = RegistrationLoot.objects.filter(pk=k)[0]
            subtotal = int(request.session['loot_cart'][k])*item.cost
            sessionLoot.append({'item':item.pk,'label':item.label,'descr':item.descr,'id':k,'count':request.session['loot_cart'][k],'subtotal':subtotal})
    for d in request.session['regs']:
        regobj = Registrant.objects.get(pk=d)
        resdata.append({'n':regobj.firstName+' '+regobj.lastName,'l':regobj.level.label,'t':regobj.total})
    return JsonResponse({"res":"ok","resdata":resdata,"lootdata":sessionLoot},safe=False)

def cartContentsHTML(request):
    sessionTotal = 0
    sessionRegs = []
    sessionLoot = []
    lootTotal = 0
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    if 'loot_cart' in request.session:
        for k in request.session['loot_cart']:
            item = RegistrationLoot.objects.get(pk=k)
            subtotal = int(request.session['loot_cart'][k])*item.cost
            sessionLoot.append({'item':item,'id':k,'count':request.session['loot_cart'][k],'subtotal':subtotal})
            lootTotal += Decimal(subtotal)
    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal,'sessionLoot':sessionLoot,'lootTotal':lootTotal}
    return render(request,"registrar/render_cart_contents.html",context)

def removeFromCart(request,itm):
    if itm in request.session['regs']:
        request.session['regs'].remove(itm)
        request.session.modified = True
    return JsonResponse({"res":"ok"},safe=False)

def removeLootFromCart(request,itm):
    if itm in request.session['loot_cart']:
        del  request.session['loot_cart'][itm]
        request.session.modified = True
    return JsonResponse({"res":"ok"},safe=False)

def merchForm1(request):
    vhost,community = vhosts.get_vhost_and_community(request)


    if request.user.is_authenticated:
        regform = RegistrantForm(user=request.user,community=community)
    else:
        regform = RegistrantForm()
    condform = ConditionsForm()
    sessionRegs = []
    sessionTotal = Decimal(0)

    if "loot" not in request.session:
        request.session["loot"] = []
        request.session["loot_cart"] = []
    event_data = EventCommunityMapping.objects.get(community=community)

    if 'regs' in request.session:
         for d in request.session['regs']:
            regobj = Registrant.objects.get(pk=d)
            level = regobj.level
            reg_data = regobj.__dict__

            sessionTotal += Decimal(regobj.total)
            reg_data["loot"] = []
            reg_data["level"] = regobj.level.label
            reg_data["level_cost"] = regobj.level.cost
            lootobj = RegistrationLevelLoot.objects.filter(level=level)
            if len(lootobj) > 0:
                for lobj in lootobj:
                    request.session["loot"].append({'reg':str(regobj.pk),'loot':str(lobj.pk)})
                    reg_data["loot"].append(lobj)
            sessionRegs.append(reg_data)
    regcount = len(sessionRegs)
    pobj = RegistrationLoot.objects.filter(event=event_data.event,active=True,purchasable=True)
    purchasable = pobj.values()
    for p in purchasable:
        lootid = f"{p['id']}"
        if lootid in request.session["loot_cart"]:
            p["count"] = request.session["loot_cart"][lootid]

        else:
            p["count"] = 0
    #print(sessionRegs)
    context = {'regform':regform,'condform':condform,'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal,'event':event_data.event,'community':community,'purchasable':purchasable,'active_2':True,'active_1':True,'is_logged_in':request.user.is_authenticated}
    return render(request,"registrar/form2.html",context)


def checkout(request):
    vhost,community = vhosts.get_vhost_and_community(request)
    sessionRegs = []
    sessionLoot = []
    sessionTotal = 0
    lootTotal = 0
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    if 'loot_cart' in request.session:
        for loot in request.session["loot_cart"].keys():
            if loot:
                loot_item = RegistrationLoot.objects.get(pk=loot)
                count = int(request.session["loot_cart"][loot])
                sessionLoot.append({'id':loot,'item':loot_item,'count':count,'subtotal':count*loot_item.cost})
                lootTotal += Decimal(loot_item.cost*count)

    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionLoot':sessionLoot,'sessionTotal':sessionTotal,'lootTotal':lootTotal,'total':sessionTotal+lootTotal,'community':community,'active_1':True,'active_2':True,'active_3':True}
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
            log.info(f"Preparing Stripe request for: {regobj}, with level {regobj.level} and price {regobj.level.stripe_price_test}")
            line_items.append({'price':regobj.level.stripe_price_test,'quantity':1})
        else:
            log.info(f"Preparing Stripe request for: {regobj}, with level {regobj.level} and price {regobj.level.stripe_price}")
            line_items.append({'price':regobj.level.stripe_price,'quantity':1})
        # if they set up donations...
        if 'loot_cart' in request.session:
            for loot in request.session['loot_cart'].keys():
                loot_item = RegistrationLoot.objects.get(pk=loot)
                count = request.session['loot_cart'][loot]*1
                if (settings.PAYMENT_STRIPE_TEST == True):
                    log.info(
                        f"Preparing Stripe request for: {loot_item}, quantity {count} price {loot_item.stripe_price_test}")
                    line_items.append({'price': loot_item.stripe_price_test, 'quantity': count})
                else:
                    log.info(
                        f"Preparing Stripe request for: {loot_item}, quantity {count} price {loot_item.stripe_price}")
                    line_items.append({'price': loot_item.stripe_price, 'quantity': count})
                fulfillment = RegistrantLootFulfillment(registrant=regobj,loot=loot_item,count=count,event=regobj.event)
                fulfillment.save()

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
    #print(event['data'])
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
        #regEvent = Event.objects.get(pk=cur_event_pk)
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
                        event=regobj.event,
                        rUUID=regobj.uuid,
                        displayId=str(regobj.uuid),
                        formId='Ply+UFLSReg-v1.0',
                        formName='Ply+UFLS Registrar',
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
                        conRegLevel=regobj.level
                    )
                    if regobj.profile:
                        registration.profile = regobj.profile
                    registration.save()

                    #Generate Loot fullfilment requests:
                    # First, activate existing fulfilment requests:
                    efr = RegistrantLootFulfillment.objects.filter(registrant=regobj)
                    for ef in efr:
                        ef.active = True
                        ef.save()
                    # Now create level-dependent loot requests if necessary:
                    lootobj = RegistrarLevelLootView.objects.filter(registrar=regobj.level.pk)
                    if len(lootobj) > 0:
                        for lobj in lootobj:
                            request.session["loot"].append({'reg': regobj.pk, 'loot': lobj.pk})
                            fulfillment = RegistrantLootFulfillment(registrant=regobj, loot=lobj.loot, quantity=lobj.count,active=True)
                            fulfillment.save()


    return HttpResponse(status=200)




def success(request):
    vhost, community = vhosts.get_vhost_and_community(request)
    sessionRegs = []
    sessionLoot = []
    sessionTotal = 0
    if 'regs' in request.session:
         for d in request.session['regs']:
             regobj = Registrant.objects.get(pk=d)
             sessionRegs.append(regobj)
             lootobjs = RegistrantLootFulfillment.objects.filter(registrant=regobj,active=True)
             sessionLoot.append(lootobjs)
             sessionTotal += Decimal(regobj.total)
    regcount = len(sessionRegs)
    #request.session['regs'] = []
    request.session.modified = True
    context = {'sessionRegs':sessionRegs,'sessionRegCount':regcount,'sessionTotal':sessionTotal,'sessionLoot':sessionLoot,'community':community}
    return render(request,"registrar/success.html",context)

