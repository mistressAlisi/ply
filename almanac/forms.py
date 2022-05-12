from django import forms
from martor.fields import MartorFormField
from dynapages.models import Templates
from almanac.models import AlmanacPage
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
    page_contents = MartorFormField()


class NewCategoryForm(forms.Form):
    icon = forms.CharField(label='Category Icon:',help_text="The Font Awesome Icon for this Category: 'fa-solid fa-layer-group' ")
    title = forms.CharField(label='Category Title:',help_text="The Title for this Category: 'My Category'")
    tooltip = forms.CharField(label='Category Tooltip:',help_text="Tooltip will be shown with mouse hover over title")

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
