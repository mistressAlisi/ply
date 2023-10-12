from django import forms
from media.gallery.core.models import GalleryItemsByCollectionPermission
from ply.toolkit import profiles
class WidgetForm(forms.Form):
    profile = False
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
            self.profile = profiles.get_active_profile(request)
        super().__init__(*args, **kwargs)
        ITEMS = []
        if (self.profile is not False):
            items = GalleryItemsByCollectionPermission.objects.filter(profile=self.profile,gif_thumbnail=False)
            for item in items:
                ITEMS.append((item.gci_uuid,item.gci_title))
            self.fields['item'].choices = ITEMS


    item = forms.ChoiceField(label='Select Gallery Item:')
    title = forms.CharField(max_length=100,label='Enter Widget Title:')
    caption = forms.CharField(max_length=500,label='Enter Widget Caption:')

