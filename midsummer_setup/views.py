from django.shortcuts import render

# Create your views here.

def setup_base(request):
    return render(request, 'setup_landing.html')

def setup_step1(request):
    return render(request, 'setup_wizard.html')