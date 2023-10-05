from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

from furry.models import Profile, RegistrantAssociationKey
from registration.models import RegistrantData, Event

from registration.serializers import RegistrantDataSanitizedUserReleaseSerializer


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def getMyRegistrations(request):

    profile = get_object_or_404(Profile, user=request.user)

    year = request.GET['event']

    registrations = []
    for x in RegistrantData.objects.filter(account=profile, event=get_object_or_404(Event, pk=year)).order_by('event'):
        registrations.append(RegistrantDataSanitizedUserReleaseSerializer(instance=x).data)

    return JsonResponse(registrations, safe=False)

@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def uploadNewImageTwentyTwo(request, orderDisplayId):
    profile = get_object_or_404(Profile, user=request.user)
    registrant = get_object_or_404(RegistrantData, account=profile, displayId=orderDisplayId)

    #print("1", request.body)
    #print("3", request.FILES)

    registrant.customUploadPicture = request.FILES.get('0')

    registrant.isCustomPicture = True
    registrant.save()

    return JsonResponse({"status": "lmao"})

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def associateNewId(request, orderDisplayId):
    profile = get_object_or_404(Profile, user=request.user)
    registrants = RegistrantData.objects.filter(orderNumber=orderDisplayId)
    email = False
    for registrant in registrants:
        if(profile.user.email.lower() != registrant.conEmail.lower()):
            if(RegistrantAssociationKey.objects.filter(account=profile, used=False).count() > 5):
                send_mail(subject="Furrydelphia Dashboard - Bad Actor",
                          message="Bad Actor Detected Account %s has been disabled." % (profile.user.email),
                          recipient_list=['cto@furrydelphia.org'],
                          from_email='Furrydelphia Dashboard <bots@furrydelphia.org>')
                send_mail(subject="Furrydelphia Dashboard - Account Disabled",
                          message="Your UFLS account was flagged as having too many open association requests and has been deactivated. The Software Team has been Notified.",
                          recipient_list=[profile.user.email],
                          from_email='Furrydelphia Dashboard <bots@furrydelphia.org>')
                profile.user.is_active = False
                profile.user.save()
                return JsonResponse({"status": "badactor"})
            assoc = RegistrantAssociationKey.objects.create(
                account=profile,
                registrant=registrant
            )

            msg = """
            Hello!<br>
            <br>
            Someone (Hopefully you) requested to associate one of your registration records with their UFLS account. This e-mail was sent to this e-mail address because the e-mail address of the UFLS account (%s) doesn't match the e-mail address used during registration (%s).<br><br>
            If this was intended, great! You can verify the transfer by clicking this link: https://backend.furrydelphia.org/account/my/registrations/associate-validation/%s/<br>
            <br>
            If this was not you, you can safely ignore this e-mail and no actions will be taken.<br>
            <br>
            Thanks,<br>
            Furrydelphia
            <hr>
            Questions? This e-mail is unmonitored. To ask for help, please e-mail software@furrydelphia.org
            """ % (profile.user.email.lower(), registrant.conEmail.lower(), assoc.key)

            send_mail(subject="Furrydelphia Dashboard - Please verify your registration association request", message="Please enable HTML messages.", html_message=msg, recipient_list=[registrant.conEmail.lower()], from_email='Furrydelphia Dashboard <bots@furrydelphia.org>')
            email = True
        else:
            registrant.account = profile
            registrant.save()
    r = "done"
    if email:
        r = "email"
    return JsonResponse({"status": r})

def associateNewIdEmailVerification(request, key):
    assoc = get_object_or_404(RegistrantAssociationKey, key=key)

    if(assoc.used):
        return HttpResponse("Key already used to associate.")
    assoc.used = True
    registrant = get_object_or_404(RegistrantData, pk=assoc.registrant.pk)

    registrant.account = assoc.account
    registrant.save()
    assoc.save()
    return redirect("https://dashboard.furrydelphia.org/dashboard")