from django import forms
from core.dynapages.models import Templates
from content_manager.almanac.models import AlmanacPage
from communities.stream.models import Stream,StreamType
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



class CreateStreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ('name','tag','descr','streamtype','type','profile','community')
        help_texts = {
            'name': ('The Human readable name of the Stream or Game room.'),
            'tag': ('Unique tag to find and share the stream'),
            'descr': ('A longer description of the  stream / game room'),
            'streamtype': ('Stream / Game Room Type'),

        }
        error_messages = {
            'name': {
                'blank': ("Cannot be blank!"),
            },
            'tag': {
                'blank': ("Cannot be blank!"),
            },
            'streamtype': {
                'blank': ("Cannot be blank!"),
            }
        },
        widgets = {
            'name': forms.TextInput(attrs={}),
            'tag': forms.TextInput(attrs={}),
            'descr': forms.TextInput(attrs={}),
            'streamtype':forms.Select(),
            'type':forms.HiddenInput(),
            'profile':forms.HiddenInput(),
            'community':forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        community = kwargs.pop('community')
        profile = kwargs.pop('profile')
        super(CreateStreamForm,self).__init__(*args,**kwargs)
        types = []
        types.append(('-1','Select Type!'))
        #try:
        ss = StreamType.objects.filter(community=community)
        for s in ss:
            types.append((s.uuid,f'[{s.name}]->|{s.descr}|'))
        # Workaround to allow installation on blank databases:
        #except:
        #    pass
        self.fields["streamtype"].choices=types
        self.fields["profile"].initial = profile.uuid
        self.fields["type"].initial = 'GAMEROOM'
        self.fields["community"].initial = community.uuid
