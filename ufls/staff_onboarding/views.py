import os
import uuid, urllib3

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from microsoftgraph.client import Client

from staff.models import Department, StaffApplication, StaffAssignment

from .forms import StaffOnboardRecordForm
from .models import StaffOnboardRecord

# Create your views here.


def appConvert(request, applicationRecord):
    app = StaffApplication.objects.filter(pk=applicationRecord).first()
    department = None
    try:
        department = app.openPosition.department
    except:
        print("No Department")

    app.closeApp = True
    app.save()

    rank = "Staff"

    c = StaffOnboardRecord.objects.create(
        firstName=app.firstName,
        lastName=app.lastName,
        fanName=app.fanName,
        dateOfBirth=app.dateOfBirth,
        email=app.email,
        telegramHandle=app.telegramHandle,
        department=None,
        rank=rank,
        title="",
    )
    return redirect("onboarding:setup", onboardRecord=c.pk)

def appMark(request, applicationRecord):
    app = StaffApplication.objects.filter(pk=applicationRecord).first()
    department = None
    try:
        department = app.openPosition.department
    except:
        print("No Department")

    title = "Staff"
    if(app.openPosition):
        rank = app.openPosition.name

    app.closeApp = True
    app.save()

    c = StaffOnboardRecord.objects.create(
        firstName=app.firstName,
        lastName=app.lastName,
        fanName=app.fanName,
        dateOfBirth=app.dateOfBirth,
        email=app.email,
        telegramHandle=app.telegramHandle,
        department=department,
        rank="Staff",
        title=title,
    )
    return redirect("front:department", pk=department.pk) or redirect("front:portal")

def appDecline(request, applicationRecord):
    app = StaffApplication.objects.filter(pk=applicationRecord).first()
    department = None
    try:
        department = app.openPosition.department
    except:
        print("No Department")

    app.closeApp = True
    app.save()

    return redirect("front:department", pk=department.pk) or redirect("front:portal")

def deleteRecord(request, onboardRecord):
    onR = get_object_or_404(StaffOnboardRecord, pk=onboardRecord)
    onR.delete()
    return redirect("front:hr")

def commitChanges(request, onboardRecord):
    if request.method == "POST":
        onR = get_object_or_404(StaffOnboardRecord, pk=onboardRecord)
        pn = StaffOnboardRecordForm(request.POST, instance=onR)
        if pn.is_valid():
            px = pn.save()

            # save to session
            response = redirect("onboarding:start-authorize")
            response.set_cookie("onboarding_record", px.pk)
            return response
    else:
        onR = get_object_or_404(StaffOnboardRecord, pk=onboardRecord)
        form = StaffOnboardRecordForm(
            instance=get_object_or_404(StaffOnboardRecord, pk=onboardRecord)
        )
        context = {
            "form": form,
            "action": "/onboarding/setup/%s/" % (onR.pk),
        }
        return render(request, "newCommit.html", context=context)


def startAuthorize(request):
    client = Client(
        os.environ.get("AAD_APP_ID"),
        os.environ.get("AAD_SECRET"),
        account_type="507af2f2-d663-4294-8d68-d5266416025a",
    )
    url = client.authorization_url(
        "https://staff.furrydelphia.org/onboarding/return/authorize/",
        ["User.ReadWrite.All"],
        state=None,
    )
    return redirect(url)


def returnAuthorize(request):
    code = request.GET["code"]
    client = Client(
        os.environ.get("AAD_APP_ID"),
        os.environ.get("AAD_SECRET"),
        account_type="507af2f2-d663-4294-8d68-d5266416025a",
    )
    response = client.exchange_code(
        "https://staff.furrydelphia.org/onboarding/return/authorize/", code
    )
    client.set_token(response.data)

    rid = request.COOKIES.get("onboarding_record")

    record = get_object_or_404(StaffOnboardRecord, pk=rid)

    record.codedPassword = "%s" % (uuid.uuid4())

    userCreationData = {
        "accountEnabled": True,
        "department": record.department.name,
        "displayName": record.displayName(),
        "givenName": record.firstName,
        "jobTitle": record.staffTitle(),
        "mailNickname": record.userProfileName().replace("@staff.furrydelphia.org", ""),
        "passwordPolicies": "DisablePasswordExpiration",
        "passwordProfile": {
            "password": record.codedPassword,
            "forceChangePasswordNextSignIn": True,
        },
        "preferredLanguage": "en-US",
        "surname": record.lastName,
        "mobilePhone": record.phone,
        "usageLocation": "US",
        "companyName": "Furrydelphia, Inc.",
        "userPrincipalName": record.userProfileName(),
    }

    res3 = client._post(client.base_url + "users", json=userCreationData)

    license = {
        "addLicenses": [{"skuId": "3b555118-da6a-4418-894f-7df1e2096870"},{"skuId": "f30db892-07e9-47e9-837c-80727f46fd3d"}],
        "removeLicenses": [],
    }

    res4 = client._post(
        client.base_url
        + "users/%s/assignLicense" % (userCreationData["userPrincipalName"]),
        json=license,
    )

    # now create the user in Staff Portal to assign them to their department.

    User = get_user_model()
    user = User.objects.create(
        username=userCreationData["userPrincipalName"],
        email=userCreationData["userPrincipalName"],
        first_name=record.firstName,
        last_name=record.lastName,
    )

    assign = StaffAssignment.objects.create(
        user=user, department=record.department, rank=record.rank, title=record.title
    )

    record.created = True
    record.save()


    em = """

    Hi %s,<br>
    <br>
    Welcome aboard to Furrydelphia! We're excited to have you as a part of our staff. To get started, we have created a Staff Account for you as well as alerted HR to begin your onboarding process.<br><br>
    <ul>
        <li>Provided Name: %s %s</li>
        <li>Furry/Fan Name: %s</li>
        <li>Department: %s</li>
        <li>Rank/Title: %s</li>
        <li>Your Supervisor: %s</li>
        <li>Your Board Member: %s</li>
    </ul>

    <hr>
    <br>
    Your staff account can be used on all systems where UFLS (Unified Furrydelphia Login System) is used. <strong>In order to use this account, you will select 'Furrydelphia Staff Login' and enter your full staff e-mail.</strong> For more information on UFLS, visit: https://ufls.furrydelphia.org/staff<br><br>

    As part of your onboarding, we have created the following account for you:<br>
    <ul>
        <li>Staff E-mail: %s</li>
        <li>Staff Username: %s</li>
        <li>Password: <code>%s</code></li>
        <li>You will be prompted to change your password on first sign in.</li>
    </ul>
    Please login to the Staff Portal with these credentials to review what you need to do next.<br>
    <a href="https://staff.furrydelphia.org/">https://staff.furrydelphia.org/</a><br>
    <br>
    <strong>Next Actiond: 1. We use Telegram for all staff communication. <u>Please join our onboarding group at: <a href="https://t.me/+HY2ffkIw7FwzNGMx">https://t.me/+HY2ffkIw7FwzNGMx</a></u></strong>
    <br>
    <strong>2. Join the Staff Announcements Channel: <a href="https://t.me/+jKQS7vKPEwAzOWY5">https://t.me/+jKQS7vKPEwAzOWY5</a>.</strong>
    <br>
    Thank you again for your time, and we look forward to running an amazing convention with you!<br>
    <br>
    Best Wishes,<br>
    Furrydelphia Operations and HR
    <hr>
    <em>Problems with the information in this e-mail? Please reach out to software@furrydelphia.org</em>
    """ % (
        record.fanName,
        record.firstName,
        record.lastName,
        record.fanName,
        record.department.name,
        record.staffTitle(),
        record.department.departmentHead.username,
        record.department.departmentBoard,
        record.userProfileName(),
        record.userProfileName().replace("@staff.furrydelphia.org", ""),
        record.codedPassword,
    )

    send_mail(
        "Staff Onboarding - Welcome to Furrydelphia!",
        "HTML E-mail",
        "Furrydelphia HR <bots@furrydelphia.org>",
        [record.email],
        html_message=em,
    )


    # here
    http = urllib3.PoolManager()
    r = http.request('POST',
                     'https://chat.furrydelphia.org/plugins/playbooks/api/v0/runs', fields={"name": "Employee Onboarding: %s" % (record.fanName),"owner_user_id": "hy76didi6pfo3b4a617c5sjxsw","team_id": "7gxp6dfwyfd1m884hp7wctaquw","playbook_id": "3k33cyshtff1u8zh1o3nn94hzw"}, headers={"Authorization": "Token %s" % ("kun5cm3u93gbib6kpq9gzmxq9r")})
    try:
        print(r.data)
    except:
        print("Whoops")
    return render(request, "onboarding_done.html", context={})


def doNewUserCreate(request, onboardRecord):
    get_object_or_404()
