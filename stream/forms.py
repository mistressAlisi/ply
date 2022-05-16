from django import forms
from colorful.fields import RGBColorField
from dynapages.models import Templates
from almanac.models import AlmanacPage
from stream.models import Stream
class NewPageForm(forms.Form):
    dynaPages = []
    try:
        templates = Templates.objects.filter(archived=False,blocked=False)
        for tem in templates:
            dynaPages.append((tem.template_id,tem.label))
    # Workaround to allow installation on blank databases:
    except:
        templates = []
        
    page_id = forms.CharField(label="Page ID/Node (only for display purposes)",widget=forms.HiddenInput)
    title = forms.CharField(label='Page Title:')
    introduction = forms.CharField(label='Short Introduction/TL;DR:')
    dynaPage = forms.ChoiceField(label='DynaPage Template:',choices=dynaPages)



class StreamSettingsForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['opened','bkg1','bkg2','bkg2','bkg2','opacity1','opacity2','midpoint','default_perm','bkgt','angle']

class AddPageForm(forms.Form):
    pages = []
    try:
        almanacPages = AlmanacPage.objects.filter(archived=False,blocked=False)
        for tem in almanacPages:
            pages.append((tem.page_id,tem.title))
    # Workaround to allow installation on blank databases:
    except:
        pages = []
    almanac_page = forms.ChoiceField(label='Select Page:',choices=pages)
