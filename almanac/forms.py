from django import forms
from martor.fields import MartorFormField
from dynapages.models import Templates
class NewPageForm(forms.Form):
    templates = Templates.objects.filter(archived=False,blocked=False)
    dynaPages = []
    for tem in templates:
        dynaPages.append((tem.template_id,tem.label))
    title = forms.CharField(label='Page Title:')
    introduction = forms.CharField(label='Short Introduction/TL;DR:')
    dynaPage = forms.ChoiceField(label='DynaPage Template:',choices=dynaPages)
    page_contents = MartorFormField()
