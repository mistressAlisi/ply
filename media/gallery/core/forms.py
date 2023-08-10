from django import forms
from django.forms import TextInput, Select,CheckboxInput,HiddenInput,PasswordInput
from media.gallery.core.models import GalleryCollectionPermission
OPERATIONS = [
    ('c', 'Copy to selected collection.'),
    ('m', 'Move to selected collection.')
]

REM_OPERATIONS = [
    ('c', 'Remove from Current Collection ONLY.'),
    ('r', 'Remove from ALL COLLECTIONS and DESTROY item.')
]

class copy_move_form(forms.Form):
    def __init__(self,*args,**kwargs):
        profile = kwargs.pop('profile')
        community = kwargs.pop('community')
        item = kwargs.pop('item')
        icol = kwargs.pop('icol')
        collections  = GalleryCollectionPermission.objects.filter(profile=profile,community=community,owner=True)
        super(copy_move_form,self).__init__(*args,**kwargs)
        CHOICES = [
            ('-1','***New Collection***')
        ]
        for col in collections:
            CHOICES.append((col.collection.uuid,col.collection.label))
        self.fields['collection'].choices = CHOICES
        self.fields['item'].initial = item
        self.fields['icol'].initial = icol




    operation = forms.ChoiceField(widget=Select(attrs={"id":"operation"}),label="Move or Copy:",help_text="Move or Copy the item to Destination?",choices=OPERATIONS)
    collection = forms.ChoiceField(widget=Select(attrs={"id":"collection"}),label="To Collection:",help_text="Target Collection for operation: select 'new' to create a new one.")
    new_collection = forms.CharField(widget=TextInput(attrs={"id":"new_collection"}),label="New Collection:",help_text="The name for the new collection (only used in 'new').",required=False)
    cast_to_stream = forms.BooleanField(widget=CheckboxInput(attrs={"id":"cast"}),label="Cast to Stream?",help_text="Shall the new item in the new collection be cast to your stream?",required=False)
    item = forms.CharField(widget=HiddenInput(attrs={'id':'item'}))
    icol = forms.CharField(widget=HiddenInput(attrs={'id':'icol'}))


class remove_form(forms.Form):
    def __init__(self,*args,**kwargs):
        profile = kwargs.pop('profile')
        community = kwargs.pop('community')
        item = kwargs.pop('item')
        icol = kwargs.pop('icol')
        super(remove_form,self).__init__(*args,**kwargs)
        self.fields['item_name'].help_text = f"Please type in the first 4 chars of this piece's ID: '{str(item)[:4]}' to continue."
        CHOICES = [
            ('r','Remove from ALL collections; and destroy item.')
        ]
        CHOICES.insert(0,('i',f"Remove only from '{icol.label}'."))
        self.fields['operation'].choices = CHOICES
        self.fields['item'].initial = item
        self.fields['icol'].initial = icol.uuid

    item_name = forms.CharField(widget=TextInput(attrs={"id":"item_name"}),label="First 4 Chars of the Item ID to be Deleted:",help_text="Will be Overriden by super",required=False)
    operation = forms.ChoiceField(widget=Select(attrs={"id":"operation"}),label="Delete/remove one or all?:",help_text="Delete THIS instance or ALL instances of this item?")
    confirm = forms.BooleanField(widget=CheckboxInput(attrs={"id":"confirm1"}),label="Delete/destroy?",help_text="Boilerplate confirmation legend here.")
    pw = forms.CharField(widget=PasswordInput(attrs={"id":"pw"}),label="Enter Password:",help_text="Ok! You're sure - enter your password please!")
    item = forms.CharField(widget=HiddenInput(attrs={'id':'item'}))
    icol = forms.CharField(widget=HiddenInput(attrs={'id':'icol'}))

