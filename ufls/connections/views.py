import base64
import json, codecs
import pickle

import requests
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Random import get_random_bytes
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from django_auth_oidc.views import login
from staff.models import StaffAssignment
from .models import Application, OTPKey, ReservationKey
from ufls.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

from Cryptodome.PublicKey import RSA
from Cryptodome.Util import asn1
from base64 import b64decode

def checkStaffEligible(email):
    r = requests.get("https://staff.furrydelphia.org/api/staff/%s/" % email, headers={"Authorization": "Token %s" % ("7d2c55e35dcddfed445218e9081831755553dcbd")})
    n = r.json()
    if(len(n) == 0):
        return False
    else:
        return True

# Create your views here.
def getScope(request, key, rapid=None):
    x = get_object_or_404(Application, code=key, enabled=True)
    user = request.user
    if(x.staff_only == True and checkStaffEligible(user.username) == False):
        return render(request, 'denied.html', {"app": x})
    y = OTPKey.objects.create(user=user,application=x)
    return render(request, 'authorize.html', {'user': request.user, 'app': x, 'otp': y, 'rapid': rapid})


def collectPermissions(user):
    m = StaffAssignment.objects.filter(user=user)
    if(m.count() == 0):
        return None
    permissions = {
        "staff-portal": {"view": False, "edit": False, "manage": False},
        "volunteer-portal": {"view": False, "edit": False, "manage": False},
        "events-manage": {"view": False, "edit": False, "manage": False},
        "app-manage": {"view": False, "edit": False, "manage": False},
        "registration-manage": {"view": False, "edit": False, "manage": False},
        "marketplace-manage": {"view": False, "edit": False, "manage": False},
        "staff-manage": {"view": False, "edit": False, "manage": False},
        "volunteer-manage": {"view": False, "edit": False, "manage": False}
    }
    for x in m:
        for key in x.permissions_matrix:
            for key2 in x.permissions_matrix[key]:
                if(x.permissions_matrix[key][key2] is True):
                    permissions[key][key2] = True
    return permissions

def fetchByOTPKey(request, key, otp):
    app = get_object_or_404(Application, code=key, enabled=True)
    x = get_object_or_404(OTPKey, application=app, key=otp)
    user = x.user
    groups = []
    for m in user.groups.all():
        groups.append(m.name)
    key, created = Token.objects.get_or_create(user=user)
    refresh = RefreshToken.for_user(user, collectPermissions(user))
    res = {
        "username": user.username,
        "groups": groups,
        "is_staff": user.is_staff,
        "isStaff": user.is_staff,
        "auth_token": key.key,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "permissions": collectPermissions(user),
        "pk": user.pk
    }
    x.delete()
    return JsonResponse(res, safe=False)

def getReservation(request, email, key):
    reservation = ReservationKey.objects.filter(key=key, email=email, reservation={}).first()
    if(reservation != None):
        obj = {
            "key": reservation.key,
            "email": reservation.email,
            "errors": []
        }
    else:
        obj = {
            "errors": ["This registration link has already been used."]
        }
    return JsonResponse(obj, safe=False)

@csrf_exempt
def postReservation(request, email, key):
    reservation = ReservationKey.objects.filter(key=key, email=email, reservation={}).first()
    if(reservation != None):

        dn = json.loads(request.body)

        pubkey = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCTnWF2Md7BNvQtEG4A3D2EEd7611tfmN4CrDM/Ze7lTIEk0xAGb3Pm5ua69dFnBvGGz+iMiBYLG91v3gIpgvE3APpIEi+cyQAbgZFAHPjpVntX32iLS0MltJAmcBKTyK5JVMjWTRvQCygOsqL5zSzyJiQBMo+AqX/sBHf3kVyr5aPA7LXltA2wA1feo94mqZsO5T4iQfydao2SOmcRD8JS8FqM0xQXUB8+tcn0fk3t2P+BO0LJBpRCJ9BO0/1kHqNDmO+4OxP0n67xi9ObMm8RDMKWEFRnGp3SyO//YxgHGNT7hXQTJwDI3qDEkScZdfy6xtVb/k6jOdbSQ7Uj60yL yuu@izumi.teamhouse.network"
        #keyDER = b64decode(pubkey)
        #seq = asn1.DerSequence()
        #seq.decode(keyDER)
        keyPub = RSA.importKey(open('/app/keys/furrydelphiareservations_rsa.pub').read())

        session_key = get_random_bytes(16)

        cipher_rsa = PKCS1_OAEP.new(keyPub)
        enc_session_key = cipher_rsa.encrypt(session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(str(dn['credit_card_number']+'.../...'+dn['credit_card_exp_date']+'.../...'+dn['credit_card_first_name']+'.../...'+dn['credit_card_last_name']).encode('utf-8'))

        reservation.reservation = dn

        reservation.reservation['credit_card_number'] = "Encrypted"
        reservation.reservation['credit_card_exp_date'] = "Encrypted"
        reservation.reservation['credit_card_first_name'] = "Encrypted"
        reservation.reservation['credit_card_last_name'] = "Encrypted"
        pkl = (enc_session_key, cipher_aes.nonce, tag, ciphertext)
        reservation.reservation['cipher_pickle'] = codecs.encode(pickle.dumps(pkl), 'base64').decode()

        reservation.save()

        obj = {
            "key": reservation.key,
            "email": reservation.email,
            "errors": [],
            "success": "Your reservation has been submitted. You will receive a confirmation e-mail from our system. When the hotel confirms your reservation, you will receive an e-mail from Marriott."
        }

        send_mail(subject='Furrydelphia 2023 Pre-Reservation System - Received Form Acknowledgement', message='This is an automated message to inform you that we have successfully received and saved your pre-reservation form. This data will be on file with Furrydelphia, Inc. until 6/1/2023. For help, reach out to bookings@furrydelphia.org and reference reservation key: %s. Please do not reply. This e-mail is unmonitored.' % (reservation.key), recipient_list=[reservation.email], from_email='bots@furrydelphia.org')

        return JsonResponse(obj, safe=False)
    else:
        obj = {
            "errors": ["This reservation link has already been used. Your reservation was not saved."]
        }
        return JsonResponse(obj, safe=False)