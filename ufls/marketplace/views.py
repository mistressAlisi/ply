import os
import uuid

import requests
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from square.client import Client

from event.models import Invoice
from registration.models import Event
from .models import Dealer, TableSize
from .serializers import DealerSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def submitDealersApp(request):
    s = DealerSerializer(instance=request.body)
    if s.is_valid():
        dealerm: Dealer = s.save()
        ev = Event.objects.filter(pk=os.getenv("CURRENT_EVENT_PK")).first()
        dealerm.event = ev
        tbl = TableSize.objects.filter(pk=s.initial_data['table_size']).first()
        dealerm.table_size = tbl
        dealerm.save()
    return Response(status=HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def getDealerApp(request):
    d = get_object_or_404(Dealer, user=request.user)
    return JsonResponse(DealerSerializer(d).data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def invoiceSquareData(request, pk):
    # beginning square connection

    client = Client(
        access_token='EAAAEHQfB2w5_II99HGjsWfF2ME2b3UTkq92xdMjFhw-MYgynilOh4XlKYE8DPfF',
        environment='production',
    )

    location_id = "HCC6A91PHHAFG"

    i = get_object_or_404(Invoice, pk=pk)

    checkout_api = client.checkout

    # first, we want to check if a checkout page exists.

    if i.checkout_id != None:
        return JsonResponse({"checkout": {"checkout_page_url": "https://connect.%s.com/v2/checkout?c=%s&l=%s" % (
        "squareup", i.checkout_id, location_id)}})

    # if not, we create the checkout data and send it to square.

    # create a new idempotency key
    i.idempotency_key = uuid.uuid4()
    i.save()

    body = {}
    body['idempotency_key'] = str(i.idempotency_key)
    body['order'] = {}
    body['order']['reference_id'] = str(i.pk)
    body['order']['line_items'] = []
    body['order']['discounts'] = []
    n = 0
    for x in i.data['item_map']:
        body['order']['line_items'].append({})
        body['order']['line_items'][n]['name'] = i.data['item_details'][x]['title']
        body['order']['line_items'][n]['quantity'] = i.data['item_details'][x]['qty']
        body['order']['line_items'][n]['base_price_money'] = {}
        body['order']['line_items'][n]['base_price_money']['amount'] = int(i.data['item_details'][x]['price'])
        body['order']['line_items'][n]['base_price_money']['currency'] = 'USD'
        body['order']['line_items'][n]['discounts'] = []
        p = 0
        for y in i.data['item_details'][x]["discounts"]:
            body['order']['line_items'][n]['discounts'].append({})
            body['order']['line_items'][n]['discounts'][p]['name'] = i.data['item_details'][x]['discounts'][p][1]
            body['order']['line_items'][n]['discounts'][p]['percentage'] = str(
                i.data['item_details'][x]['discounts'][p][0])
            p += 1
        n += 1
    t = 0
    body['order']['taxes'] = []
    for x in i.data['taxes']:
        body['order']['taxes'].append({})
        body['order']['taxes'][t]['name'] = i.data['taxes'][t][1]
        body['order']['taxes'][t]['percentage'] = str(i.data['taxes'][t][0])
        t += 1

    for discount in i.data['discounts']:
        body['order']['discounts'].append({
          "uid": "discount-%s" % discount['percentage'],
          "name": discount['name'],
          "percentage": discount['percentage'],
          "scope": "ORDER"
        })


    body['ask_for_shipping_address'] = False
    body['merchant_support_email'] = "marketplace@furrydelphia.org"
    body['pre_populate_buyer_email'] = i.user.username
    body['redirect_url'] = 'https://backend.furrydelphia.org/api/v1/mkt/functions/square/order-confirm/'

    result = checkout_api.create_checkout(location_id, body)

    if result.is_success():
        i.checkout_id = result.body['checkout']['id']
        i.save()

    return JsonResponse(result.body)


def orderConfirm(request):
    client = Client(
        access_token='EAAAEHQfB2w5_II99HGjsWfF2ME2b3UTkq92xdMjFhw-MYgynilOh4XlKYE8DPfF',
        environment='production',
    )

    location_id = "HCC6A91PHHAFG"

    checkout_id = request.GET.get('checkoutId')
    reference_id = request.GET.get('referenceId')
    transaction_id = request.GET.get('transactionId')

    orders_api = client.orders

    body = {}
    body['order_ids'] = [transaction_id]

    result = orders_api.batch_retrieve_orders(location_id, body)

    i = get_object_or_404(Invoice, pk=reference_id)

    if result.is_success():
        # paid logic goes here
        if result.body['orders'][0]['state'] == "COMPLETED":
            # paid successfully.
            i.square_code = transaction_id
            i.amount_collected = result.body['orders'][0]['total_money']['amount']
            i.paid = True
            i.date_paid = timezone.now()
            i.debug_result_data = result.body

            i.save()

            if i.invoice_type == "table":
                dealer = Dealer.objects.get(account=i.user, event=Event.objects.get(pk=3))
                dealer.paid = True
                t = """
			<p>Dear %s,</p>
			<p>Thank you for paying for your Dealers Den Table for %s. Your Receipt from Square will be available for you to review in a seperate e-mail.</p>
			<p>Your registration codes are now available to use for %s. To get started, visit: <a href="https://app.furrydelphia.org/marketplace">https://app.furrydelphia.org/marketplace</a></p>
			<p>Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://app.furrydelphia.org/marketplace">https://app.furrydelphia.org/marketplace</a><br><br>
			Thanks, and stay Safe!</p>
<br>
- Fawkes, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org
			""" % (dealer.business_name, dealer.event.name, dealer.event.name)

                send_mail("ACTION REQUIRED - %s - Registration Codes for %s" % (dealer.event.name, dealer.event.name),
                          'Please enable HTML Messages.', 'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [dealer.account.username], html_message=t)
                dealer.save()

            return redirect("https://app.furrydelphia.org/marketplace")
        else:
            return JsonResponse(result.body)
    elif result.is_error():
        # redirect logic goes here
        return JsonResponse(result.body)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def signGenerate(request):

    dealer = Dealer.objects.get(account=request.user, event=Event.objects.get(pk=3))

    if dealer.contract_url is not None:
        return JsonResponse({"sign_url": dealer.contract_url})

    signa = {
        "template_id": "75ba4182-5a2b-4af6-a6c8-1e3cdd17aeb4",
        "signers":[{"name":"%s %s" % (dealer.first_name, dealer.last_name),"email":dealer.account.username, "redirect_url": "https://backend.furrydelphia.org/api/v1/mkt/functions/sign/finish/%s/" % dealer.pk, "signature_request_delivery_method":"embedded"}],
        "placeholder_fields":[{"api_key":"vendor","value":dealer.business_name}],
        "test": "no"
    }

    r = requests.post('https://esignatures.io/api/contracts?token=c0f34328-57b8-46b2-97a2-24997b209447', json=signa)
    urlss = r.json()['data']['contract']['signers'][0]['sign_page_url']
    dealer.contract_url = urlss
    dealer.save()
    return JsonResponse({"sign_url": urlss})

def signFinish(request, pk):
    dealer = Dealer.objects.get(pk=int(pk))
    dealer.contract_signed = True
    dealer.save()
    return redirect("https://app.furrydelphia.org/marketplace")


def sendOverToDealers(request):
    return None