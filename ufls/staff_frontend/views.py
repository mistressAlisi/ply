import json

import urllib3
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import routers, serializers, viewsets, status, permissions

from staff.forms import StaffApplicationForm
from staff.models import (
    Department,
    OpenPosition,
    StaffApplication,
    StaffAssignment, LicenseKey,
)
from staff_onboarding.models import StaffOnboardRecord

# Create your views here.


def index(request):
    return render(request, "index.html", context={})


def help(request):
    return render(request, "help.html", context={})


@login_required(login_url="/ufls/login/")
def dashboard(request):

    assignments = StaffAssignment.objects.filter(user=request.user)

    return render(
        request,
        "dashboard.html",
        context={"assignments": assignments, "departments": Department.objects.all()},
    )

@login_required(login_url="/ufls/login/")
@permission_required("onboarding.can_see_hr")
def hrAppView(request, id):
    app = StaffApplication.objects.get(pk=id)
    app_form = StaffApplicationForm(instance=app)
    return render(
        request,
        "app_detail.html",
        context={
            "app": app,
            "x": app_form
        },
    )

@login_required(login_url="/ufls/login/")
@permission_required("onboarding.can_see_hr")
def hr(request):
    return render(
        request,
        "hr_portal.html",
        context={"applications": StaffApplication.objects.filter(closeApp=False, openPosition=None), "departments": Department.objects.all(), "onboardings": StaffOnboardRecord.objects.filter(created=False)},
    )


def uflsLogin(request):
    if request.method == "GET":
        return render(request, "ufls_login.html", context={})


def uflsStaffAuthentication(request):
    # ufls/staff/?uflsStaffSession=d649e37d-2947-4798-9e45-1d8a99b79b0f
    http = urllib3.PoolManager()
    if request.GET.get("uflsStaffSession"):
        r = http.request(
            "GET",
            "https://backend.furrydelphia.org/app/redirect/staff-portal/otp/%s/"
            % (request.GET.get("uflsStaffSession")),
        )

        id = json.loads(r.data.decode("utf-8"))

        User = get_user_model()
        user = User.objects.filter(username=id["username"]).first()
        if user == None:
            user = User.objects.create(
                username=id["username"], email=id["username"], is_staff=False
            )
        login(request, user)
        return redirect("front:index")
    else:
        return HttpResponse("No way Jose")

    return None

@login_required(login_url="/ufls/login/")
def distributeApps(request):
    return render(request, 'app_distributions.html', context={})

def application(request, openpk=None):
    if request.method == "POST":
        form = StaffApplicationForm(request.POST)
        if form.is_valid():
            px = form.save()
            return render(request, "thanksapp.html", context={})
    else:
        assignment = None
        if openpk != None:
            assignment = get_object_or_404(OpenPosition, pk=openpk)
        form = StaffApplicationForm(initial={"openPosition": assignment})
        return render(
            request,
            "appform.html",
            context={"form": form, "pkcheck": openpk, "assignment": assignment},
        )


def open(request):

    context = {"departments": Department.objects.all()}

    return render(request, "open.html", context=context)


def departmentList(request):
    return None


def departmentView(request, pk):
    d = get_object_or_404(Department, pk=pk)
    apps = StaffApplication.objects.filter(openPosition__department=d, closeApp=False)
    app_forms = []
    app_form_pks = []
    for x in apps:
        app_forms.append(StaffApplicationForm(instance=x))
        app_form_pks.append(x.pk)
    return render(
        request,
        "department.html",
        context={
            "apps": apps,
            "app_forms": app_forms,
            "department": d,
            "pks": app_form_pks,
        },
    )


def newTask(request, pk):
    return None


def newAnnouncement(request, pk):
    return None


def staffTaskView(request, pk):
    return None


def markStaffTaskDone(request, pk):
    return None

@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def getStaffAssignments(request, email):

    u = get_user_model().objects.filter(username=email).first()
    asn = StaffAssignment.objects.filter(user=u)

    assoc = []

    isUpperMgmt = False

    for x in asn:
        assoc.append({
            "department": x.department.name,
            "department_pk": x.department.pk,
        })
        if(x.rank != "Staff"):
            isUpperMgmt = True

    if(isUpperMgmt):
        assoc.append({
            "department": "Dept Heads",
            "department_pk": "dpthead"
        })

    return JsonResponse(assoc, safe=False)

@login_required(login_url="/ufls/login/")
def staffList(request):
    u = User.objects.all()
    s = []
    for x in u:
        s.append([x, StaffAssignment.objects.filter(user=x).first()])
    return render(request, "staffList.html", context={"staff": s, "departments": Department.objects.all()})

@login_required(login_url="/ufls/login/")
def checkAndDistribute(request, program_key):
    u = request.user
    lic = LicenseKey.objects.filter(program=program_key, assigned=u).first()
    if(lic == None):
        lic = LicenseKey.objects.filter(
            program=program_key,
            assigned=None
        ).first()
    lic.assigned = u
    lic.save()
    return render(request, "display_license.html", context={"license": lic})
